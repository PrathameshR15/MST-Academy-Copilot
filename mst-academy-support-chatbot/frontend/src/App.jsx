import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './styles/app.css'

const API_BASE = 'http://localhost:8000/api'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hello! How can I help you with Academy support?', source: null }
  ])
  const [input, setInput] = useState('')
  const [provider, setProvider] = useState('gemini')
  const [isLoading, setIsLoading] = useState(false)
  const [knowledgeStatus, setKnowledgeStatus] = useState(null)
  const [websiteStatus, setWebsiteStatus] = useState(null)
  const [isRefreshing, setIsRefreshing] = useState(false)
  
  const chatWindowRef = useRef(null)

  useEffect(() => {
    fetchStatus()
  }, [])

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight
    }
  }, [messages])

  const fetchStatus = async () => {
    try {
      const kRes = await fetch(`${API_BASE}/knowledge/status`)
      const kData = await kRes.json()
      setKnowledgeStatus(kData)

      const wRes = await fetch(`${API_BASE}/website/status`)
      const wData = await wRes.json()
      setWebsiteStatus(wData)
    } catch (error) {
      console.error("Error fetching status", error)
    }
  }

  const handleRefreshWebsite = async () => {
    setIsRefreshing(true)
    try {
      const res = await fetch(`${API_BASE}/website/refresh`, { method: 'POST' })
      await res.json()
      await fetchStatus()
    } catch (error) {
      console.error("Error refreshing website", error)
    }
    setIsRefreshing(false)
  }

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userText = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userText }])
    setIsLoading(true)

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userText, 
          history: messages.map(m => ({ role: m.role, text: m.text })),
          provider: provider 
        })
      })
      const data = await res.json()

      let sourceText = "Information not found"
      if (data.source === 'LOCAL_KB') sourceText = "Source: Academy Knowledge Base"
      else if (data.source === 'WEBSITE') sourceText = "Source: MST Academy Website"
      else if (data.source === 'BOTH') sourceText = "Source: Academy Knowledge Base + Website"

      setMessages(prev => [...prev, { 
        role: 'assistant', 
        text: data.answer, 
        source: sourceText 
      }])
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        text: "Error connecting to the support assistant. Please try again later.", 
        source: "Error" 
      }])
    }
    setIsLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleClear = () => {
    setMessages([{ role: 'assistant', text: 'Hello! How can I help you with Academy support?', source: null }])
  }

  return (
    <>
      <div className="main-container">
        <div className="header">
          <div className="header-title">
            <h1>MST Academy</h1>
            <span className="subtitle">Support Assistant</span>
          </div>
          <div className="header-actions" style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
            <select 
              value={provider} 
              onChange={(e) => setProvider(e.target.value)}
              style={{padding: '4px 8px', borderRadius: '4px', border: '1px solid #e5e7eb'}}
            >
              <option value="openai">OpenAI</option>
              <option value="gemini">Google Gemini</option>
            </select>
            <button className="clear-button" onClick={handleClear}>Clear Chat</button>
            <div className="status-indicator">
              <div className="status-dot"></div> Online
            </div>
          </div>
        </div>

        <div className="chat-window" ref={chatWindowRef}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-row ${msg.role}`}>
              <div className="message-bubble">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
              </div>
              {msg.source && msg.source !== "Error" && (
                <div className="source-badge">{msg.source}</div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message-row assistant">
              <div className="message-bubble" style={{fontStyle: 'italic', color: '#6b7280'}}>
                Assistant is typing...
              </div>
            </div>
          )}
        </div>

        <div className="chat-input-container">
          <input 
            type="text" 
            className="chat-input"
            placeholder="Ask your question..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button className="send-button" onClick={handleSend} disabled={!input.trim() || isLoading}>
            Send
          </button>
        </div>
      </div>

      <div className="settings-panel">
        <div>
          <h2>Admin / Status</h2>
          <hr style={{border: 'none', borderTop: '1px solid #e5e7eb', margin: '8px 0'}}/>
        </div>

        <div className="settings-section">
          <h3>Local Knowledge</h3>
          <div className="settings-item">
            <span className="settings-label">Files loaded:</span>
            <span className="settings-value">{knowledgeStatus?.files_loaded ?? 0}</span>
          </div>
          <div className="settings-item">
            <span className="settings-label">Status:</span>
            <span className="settings-value">{knowledgeStatus?.status ?? 'Loading...'}</span>
          </div>
        </div>

        <div className="settings-section">
          <h3>Website Knowledge</h3>
          <div className="settings-item">
            <span className="settings-label">URL:</span>
            <span className="settings-value" title={websiteStatus?.url}>{websiteStatus?.url ?? '...'}</span>
          </div>
          <div className="settings-item">
            <span className="settings-label">Cached pages:</span>
            <span className="settings-value">{websiteStatus?.cached_pages ?? 0}</span>
          </div>
          <div className="settings-item">
            <span className="settings-label">Last refreshed:</span>
            <span className="settings-value" title={websiteStatus?.last_refreshed}>
              {websiteStatus?.last_refreshed ? new Date(websiteStatus.last_refreshed).toLocaleString() : 'Never'}
            </span>
          </div>
          <div className="settings-item">
            <span className="settings-label">Status:</span>
            <span className="settings-value">{websiteStatus?.status ?? 'Loading...'}</span>
          </div>
          
          <button 
            className="refresh-button" 
            onClick={handleRefreshWebsite} 
            disabled={isRefreshing}
            style={{marginTop: '12px'}}
          >
            {isRefreshing ? 'Crawling...' : 'Refresh Website Knowledge'}
          </button>
        </div>
      </div>
    </>
  )
}

export default App
