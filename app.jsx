import React, { useState, useEffect } from 'react';
import { LogIn, LogOut, FileText, Upload, ChevronDown, List } from 'lucide-react';

// API Configuration
// NOTE: Use your final Vercel domain here!
const API_BASE_URL = 'https://silvia-munjal-three.vercel.app';
const API_ROUTES = {
  LOGIN: `${API_BASE_URL}/auth/login`,
  DOCUMENTS_LIST: `${API_BASE_URL}/portal/documents`,
  DOCUMENT_UPLOAD: `${API_BASE_URL}/portal/documents/upload`,
  QA_CHATBOT: `${API_BASE_URL}/qa-chatbot`,
};

// --- Component Schemas ---

const DocumentCard = ({ doc }) => {
  const uploadDate = new Date(doc.upload_date).toLocaleDateString();

  const getStatusColor = (status) => {
    switch (status) {
      case 'Reviewed':
        return 'bg-green-100 text-green-800';
      case 'New':
        return 'bg-blue-100 text-blue-800';
      case 'Processing':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white p-4 border border-gray-200 rounded-xl shadow-md transition hover:shadow-lg hover:border-indigo-300">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center">
          <FileText className="w-5 h-5 mr-2 text-indigo-600" />
          {doc.filename}
        </h3>
        <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(doc.status)}`}>
          {doc.status}
        </span>
      </div>
      <p className="text-sm text-gray-500 mb-3">Uploaded: {uploadDate}</p>
      
      <div className="p-3 bg-gray-50 rounded-lg border border-dashed border-gray-300">
        <p className="text-sm font-medium text-indigo-700 mb-1">LLM Summary:</p>
        <p className="text-sm text-gray-600 italic leading-relaxed">
          {doc.llm_summary || "Summary generation pending..."}
        </p>
      </div>
      
      <a 
        href={doc.cloud_path} 
        target="_blank" 
        rel="noopener noreferrer"
        className="mt-3 inline-flex items-center text-indigo-600 hover:text-indigo-800 text-sm font-medium transition duration-150"
      >
        View Secure File
      </a>
    </div>
  );
};


const DocumentUploader = ({ token, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage({ text: 'Please select a file first.', type: 'error' });
      return;
    }

    setLoading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(API_ROUTES.DOCUMENT_UPLOAD, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ text: `Success! File ${data.filename} uploaded and processing started.`, type: 'success' });
        setFile(null);
        // Refresh document list in the parent component
        onUploadSuccess(); 
      } else {
        setMessage({ text: `Upload failed: ${data.detail || response.statusText}`, type: 'error' });
      }

    } catch (error) {
      console.error('Upload error:', error);
      setMessage({ text: 'Network error during upload. Check console.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const messageClasses = message.type === 'error' ? 'text-red-600 bg-red-50' : 'text-green-600 bg-green-50';

  return (
    <div className="mt-8 p-6 bg-white rounded-xl shadow-lg border border-indigo-200">
      <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
        <Upload className="w-5 h-5 mr-2 text-indigo-600" />
        Upload New Document
      </h2>
      <form onSubmit={handleUpload}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Document (PDF, DOCX, TXT recommended)
          </label>
          <input
            type="file"
            onChange={handleFileChange}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
          />
        </div>
        
        {message.text && (
          <div className={`p-3 rounded-lg text-sm mb-4 border ${messageClasses}`}>
            {message.text}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !file}
          className="w-full py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 disabled:cursor-not-allowed transition"
        >
          {loading ? 'Uploading & Processing...' : 'Secure Upload'}
        </button>
      </form>
    </div>
  );
};


const LoginScreen = ({ setToken, setUserId }) => {
  const [email, setEmail] = useState('client@test.com');
  const [password, setPassword] = useState('password');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(API_ROUTES.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // The endpoint is defined to accept a Pydantic model (TokenRequest) via Body,
        // so we send JSON, not form data.
        body: JSON.stringify({ email, password }), 
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.access_token);
        // In a real app, you would decode the token to get the user email/ID (sub field)
        setUserId(email); 
        localStorage.setItem('authToken', data.access_token);
      } else {
        setError(data.detail || 'Login failed. Check credentials.');
      }
    } catch (err) {
      setError('Network error. Check if the backend is running.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
        <h2 className="text-3xl font-extrabold text-center text-gray-900 mb-6 flex items-center justify-center">
          <LogIn className="w-7 h-7 mr-2 text-indigo-600" />
          Client Portal Login
        </h2>
        <p className="text-center text-sm text-gray-600 mb-6">
          Use demo credentials: `client@test.com` / `password`
        </p>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="client@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="password"
            />
          </div>

          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded-lg border border-red-300">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 transition"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};


const PortalDashboard = ({ token, userId, setToken, setUserId }) => {
  const [documents, setDocuments] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [page, setPage] = useState('list'); // 'list', 'upload', 'qa'
  const [qaQuery, setQaQuery] = useState('');
  const [qaAnswer, setQaAnswer] = useState(null);
  const [loadingQa, setLoadingQa] = useState(false);
  const [qaError, setQaError] = useState('');

  const fetchDocuments = async () => {
    setLoadingDocs(true);
    try {
      const response = await fetch(API_ROUTES.DOCUMENTS_LIST, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      } else if (response.status === 401) {
        // Token expired or invalid, log out
        handleLogout(); 
      } else {
        console.error('Failed to fetch documents:', response.statusText);
      }

    } catch (error) {
      console.error('Network error fetching documents:', error);
    } finally {
      setLoadingDocs(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUserId(null);
    localStorage.removeItem('authToken');
  };

  const handleQaQuery = async (e) => {
    e.preventDefault();
    setLoadingQa(true);
    setQaAnswer(null);
    setQaError('');

    try {
      const response = await fetch(API_ROUTES.QA_CHATBOT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: qaQuery }),
      });

      const data = await response.json();

      if (response.ok) {
        setQaAnswer(data.answer);
      } else {
        setQaError(data.detail || 'AI query failed.');
      }
    } catch (error) {
      setQaError('Network error during AI query. Check console.');
    } finally {
      setLoadingQa(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchDocuments();
    }
  }, [token]);

  const renderContent = () => {
    switch (page) {
      case 'upload':
        return (
          <DocumentUploader 
            token={token} 
            onUploadSuccess={() => {
              setPage('list');
              fetchDocuments();
            }} 
          />
        );
      case 'qa':
        return (
          <div className="mt-8 p-6 bg-white rounded-xl shadow-lg border border-green-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              AI Query Assistant
            </h2>
            <form onSubmit={handleQaQuery} className="space-y-4">
              <textarea
                value={qaQuery}
                onChange={(e) => setQaQuery(e.target.value)}
                placeholder="Ask about trade compliance, dispute resolution, or contract drafting..."
                rows="3"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500"
              />
              <button
                type="submit"
                disabled={loadingQa || !qaQuery.trim()}
                className="w-full py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-green-400 transition"
              >
                {loadingQa ? 'Searching Knowledge Base...' : 'Ask AI Assistant'}
              </button>
            </form>

            {qaError && (
              <div className="mt-4 p-3 text-sm text-red-700 bg-red-100 rounded-lg border border-red-300">
                Error: {qaError}
              </div>
            )}
            {qaAnswer && (
              <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-300">
                <p className="font-semibold text-green-800 mb-1">AI Response:</p>
                <p className="text-gray-700">{qaAnswer}</p>
              </div>
            )}
            
          </div>
        );
      case 'list':
      default:
        return (
          <div className="mt-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-800 flex items-center">
                <List className="w-5 h-5 mr-2 text-indigo-600" />
                Your Documents
              </h2>
            </div>
            
            {loadingDocs ? (
              <p className="text-gray-500">Loading documents...</p>
            ) : documents.length > 0 ? (
              <div className="space-y-6">
                {documents.map((doc) => (
                  <DocumentCard key={doc.id} doc={doc} />
                ))}
              </div>
            ) : (
              <div className="p-8 text-center bg-gray-100 rounded-xl border border-dashed border-gray-300">
                <p className="text-lg text-gray-500">No documents found. Click "Upload" to add a new file.</p>
              </div>
            )}
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-indigo-600 shadow-md">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">
            Advocate Client Portal
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-white text-sm opacity-80 hidden sm:inline">User: {userId}</span>
            <button
              onClick={handleLogout}
              className="bg-white text-indigo-600 py-1.5 px-3 rounded-full text-sm font-semibold hover:bg-indigo-100 transition flex items-center shadow"
            >
              <LogOut className="w-4 h-4 mr-1" />
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="flex space-x-3 mb-6">
          <button
            onClick={() => setPage('list')}
            className={`px-4 py-2 text-sm font-medium rounded-full transition ${page === 'list' ? 'bg-indigo-600 text-white shadow-md' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
          >
            <List className="w-4 h-4 inline mr-2" />
            Document List
          </button>
          <button
            onClick={() => setPage('upload')}
            className={`px-4 py-2 text-sm font-medium rounded-full transition ${page === 'upload' ? 'bg-indigo-600 text-white shadow-md' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
          >
            <Upload className="w-4 h-4 inline mr-2" />
            Upload Document
          </button>
          <button
            onClick={() => setPage('qa')}
            className={`px-4 py-2 text-sm font-medium rounded-full transition ${page === 'qa' ? 'bg-green-600 text-white shadow-md' : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'}`}
          >
            <ChevronDown className="w-4 h-4 inline mr-2" />
            AI Assistant
          </button>
        </div>

        {renderContent()}
      </main>
    </div>
  );
};


const App = () => {
  const [token, setToken] = useState(null);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      // NOTE: In a real app, you would validate this token against the backend 
      // or decode it to get the user ID before setting state.
      // For this demo, we'll assume the token is valid and set a mock user ID.
      setToken(storedToken);
      setUserId('client@test.com'); // Re-set mock ID
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-xl text-indigo-600">Loading...</p>
      </div>
    );
  }

  return (
    <div className="font-sans antialiased">
      {token ? (
        <PortalDashboard 
          token={token} 
          userId={userId}
          setToken={setToken} 
          setUserId={setUserId}
        />
      ) : (
        <LoginScreen setToken={setToken} setUserId={setUserId} />
      )}
    </div>
  );
};

export default App;
