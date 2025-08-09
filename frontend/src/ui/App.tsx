import React, { useMemo, useRef, useState } from 'react'

type ChatMessage = { role: 'user' | 'assistant'; content: string }

async function apiPost<T>(url: string, body: any, asBlob = false): Promise<T | Blob> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return asBlob ? (await res.blob()) : ((await res.json()) as T)
}

export const App: React.FC = () => {
  // Chat state
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const chatEndRef = useRef<HTMLDivElement | null>(null)

  // Data panel state (user-provided; no hard-coding)
  const [businessDescription, setBusinessDescription] = useState('')
  const [markText, setMarkText] = useState('')
  const [classesText, setClassesText] = useState('')
  const [conflictInfo, setConflictInfo] = useState('')
  const [downloading, setDownloading] = useState(false)

  const [fullName, setFullName] = useState('')
  const [address1, setAddress1] = useState('')
  const [address2, setAddress2] = useState('')
  const [city, setCity] = useState('')
  const [province, setProvince] = useState('')
  const [postalCode, setPostalCode] = useState('')
  const [country, setCountry] = useState('South Africa')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [slogan, setSlogan] = useState('')

  const niceClasses = useMemo(() =>
    classesText
      .split(',')
      .map((s) => parseInt(s.trim(), 10))
      .filter((n) => !isNaN(n)),
    [classesText]
  )

  const scrollToEnd = () => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })

  const sendMessage = async () => {
    const text = input.trim()
    if (!text) return
    const nextMessages: ChatMessage[] = [...messages, { role: 'user', content: text }]
    setMessages(nextMessages)
    setInput('')
    setSending(true)
    try {
      const res = await apiPost<{ reply: string }>(
        '/api/triage/chat',
        { messages: nextMessages.map((m) => ({ role: m.role, content: m.content })) }
      )
      setMessages((prev) => [...prev, { role: 'assistant', content: res.reply }])
    } catch (e: any) {
      setMessages((prev) => [...prev, { role: 'assistant', content: `Error: ${e.message}` }])
    } finally {
      setSending(false)
      setTimeout(scrollToEnd, 50)
    }
  }

  const suggestClasses = async () => {
    if (!businessDescription.trim()) return
    const data = await apiPost<{ suggestions: { class_number: number; class_title: string; confidence: number }[] }>(
      '/api/classify/suggest',
      { business_description: businessDescription.trim() }
    )
    setClassesText(data.suggestions.map((s) => String(s.class_number)).join(', '))
  }

  const doConflictCheck = async () => {
    if (!markText.trim() || niceClasses.length === 0) return
    const data = await apiPost<{ status: string; disclaimer: string; items: any[] }>(
      '/api/conflict-check',
      { mark_text: markText.trim(), nice_classes: niceClasses }
    )
    setConflictInfo(`${data.status}: ${data.disclaimer}`)
  }

  const canGenerate =
    Boolean(markText.trim()) &&
    niceClasses.length > 0 &&
    Boolean(fullName.trim()) &&
    Boolean(address1.trim()) &&
    Boolean(city.trim()) &&
    Boolean(province.trim()) &&
    Boolean(postalCode.trim()) &&
    Boolean(email.trim()) &&
    Boolean(phone.trim())

  const generate = async () => {
    if (!canGenerate) return
    setDownloading(true)
    try {
      const blob = (await apiPost(
        '/api/documents/generate',
        {
          intake: {
            mark_text: markText.trim(),
            slogan: slogan.trim() || undefined,
            nice_classes: niceClasses,
            applicant: {
              full_name: fullName.trim(),
              address_line_1: address1.trim(),
              address_line_2: address2.trim() || undefined,
              city: city.trim(),
              province: province.trim(),
              postal_code: postalCode.trim(),
              country: country.trim() || 'South Africa',
              email: email.trim(),
              phone_number: phone.trim(),
            },
          },
        },
        true
      )) as Blob

      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Trademark_Package.zip'
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 360px', gap: 16, maxWidth: 1180, margin: '16px auto', padding: '0 12px', fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif' }}>
      {/* Chat column */}
      <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, minHeight: 520, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: 12, borderBottom: '1px solid #e5e7eb' }}>
          <h2 style={{ margin: 0 }}>Trademark Co-Pilot — Chat</h2>
          <div style={{ color: '#b45309', fontSize: 13 }}>Not a law firm. No legal advice. For self-filing assistance only.</div>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
          {messages.length === 0 && (
            <div style={{ color: '#64748b', fontSize: 14 }}>
              Say hello and tell me what you want to do. I will ask only for the information needed to prepare your trademark application.
            </div>
          )}
          {messages.map((m, idx) => (
            <div key={idx} style={{ margin: '10px 0' }}>
              <div style={{ fontWeight: 600, fontSize: 12, color: '#475569' }}>{m.role === 'user' ? 'You' : 'Assistant'}</div>
              <div style={{ whiteSpace: 'pre-wrap' }}>{m.content}</div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div style={{ display: 'flex', gap: 8, padding: 12, borderTop: '1px solid #e5e7eb' }}>
          <input
            aria-label="Type a message"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                sendMessage()
              }
            }}
            style={{ flex: 1, padding: '10px 12px', border: '1px solid #cbd5e1', borderRadius: 6 }}
          />
          <button onClick={sendMessage} disabled={sending || !input.trim()} style={{ padding: '10px 14px' }}>
            {sending ? 'Sending…' : 'Send'}
          </button>
        </div>
      </div>

      {/* Data panel */}
      <div style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 12 }}>
        <h3 style={{ marginTop: 4 }}>Application Data</h3>

        <div style={{ marginTop: 10 }}>
          <div style={{ fontWeight: 600 }}>Business Description</div>
          <textarea
            aria-label="Business description"
            placeholder="Describe what your business sells or offers (for class suggestion)"
            value={businessDescription}
            onChange={(e) => setBusinessDescription(e.target.value)}
            style={{ width: '100%', height: 64 }}
          />
          <button onClick={suggestClasses} disabled={!businessDescription.trim()} style={{ marginTop: 6 }}>Suggest Classes</button>
        </div>

        <div style={{ marginTop: 14 }}>
          <div style={{ fontWeight: 600 }}>Trademark</div>
          <input
            aria-label="Mark text"
            placeholder="Word mark (text)"
            value={markText}
            onChange={(e) => setMarkText(e.target.value)}
            style={{ width: '100%', marginTop: 6 }}
          />
          <input
            aria-label="NICE classes"
            placeholder="Classes (comma-separated, e.g., 25, 35)"
            value={classesText}
            onChange={(e) => setClassesText(e.target.value)}
            style={{ width: '100%', marginTop: 6 }}
          />
          <input
            aria-label="Slogan"
            placeholder="Slogan (optional)"
            value={slogan}
            onChange={(e) => setSlogan(e.target.value)}
            style={{ width: '100%', marginTop: 6 }}
          />
          <button onClick={doConflictCheck} disabled={!markText.trim() || niceClasses.length === 0} style={{ marginTop: 8 }}>Conflict Check</button>
          {conflictInfo && <div style={{ marginTop: 6, color: '#334155', fontSize: 13 }}>{conflictInfo}</div>}
        </div>

        <div style={{ marginTop: 14 }}>
          <div style={{ fontWeight: 600 }}>Applicant</div>
          <input aria-label="Applicant full name" placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Address line 1" placeholder="Address line 1" value={address1} onChange={(e) => setAddress1(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Address line 2" placeholder="Address line 2 (optional)" value={address2} onChange={(e) => setAddress2(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="City" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Province" placeholder="Province" value={province} onChange={(e) => setProvince(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Postal code" placeholder="Postal code" value={postalCode} onChange={(e) => setPostalCode(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Country" placeholder="Country" value={country} onChange={(e) => setCountry(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
          <input aria-label="Phone number" placeholder="Phone number" value={phone} onChange={(e) => setPhone(e.target.value)} style={{ width: '100%', marginTop: 6 }} />
        </div>

        <div style={{ marginTop: 16 }}>
          <button onClick={generate} disabled={!canGenerate || downloading}>
            {downloading ? 'Preparing…' : 'Generate ZIP'}
          </button>
        </div>
      </div>
    </div>
  )
} 