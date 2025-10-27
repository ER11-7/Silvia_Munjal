import React, { useState, useEffect } from 'react';
import { Aperture, BookOpen, Key, Users, MessageSquare, Briefcase, ChevronRight, Upload, FileText, Lock, CheckCircle, XCircle, Menu, X, Search, Globe, FileCheck, DollarSign } from 'lucide-react';

// --- DUMMY DATA SIMULATION (Replaces Headless CMS & FastAPI) ---
// Note: Content has been updated to reflect the 'International Business & Trade Lawyer' focus.
const DUMMY_PUBLICATIONS = [
  { id: 1, title: "Navigating Post-Brexit Trade Compliance for Indian Exporters", date: "Oct 2025", area: "Trade Contracts", summary: "An analysis of recent tariff changes and new documentation requirements for UK trade partners.", link: "#" },
  { id: 2, title: "Mitigating Risk in Cross-Border E-Commerce Agreements", date: "Sep 2025", area: "Dispute Resolution", summary: "Strategies for protecting intellectual property and ensuring payment security in digital global sales.", link: "#" },
  { id: 3, title: "The Legal Guide to Global OEM & Export Manufacturing Contracts", date: "Aug 2025", area: "Trade Contracts", summary: "Essential guide for protecting new technology and trademarks in the pre-seed funding stage.", link: "#" },
  { id: 4, title: "Understanding Bilateral Investment Treaties (BITs) in Asia", date: "Jul 2025", area: "Compliance & Advisory", summary: "A review of how BITs impact foreign investment protection and dispute settlement mechanisms.", link: "#" },
];

const DUMMY_DOCUMENTS = [
    { id: 1, name: "Master Distributor Agreement (EU).pdf", date: "2025-10-25", status: "Reviewed", summary: "LLM Summary: The document outlines exclusive distribution clauses for the EU market. Key finding: No automatic renewal clause is present." },
    { id: 2, name: "Draft Arbitration Notice - Project Beta.docx", date: "2025-10-20", status: "New", summary: "LLM Summary: A preliminary review suggests that the case is best suited for mediation under SIAC rules. Further document gathering on correspondence history is needed." },
];

const PRACTICE_AREAS = [
    "Export & Trade Contracts", "Compliance & Regulatory", "Dispute Resolution", "International Negotiations"
];

// --- NEW COLOR CODES FOR CLASSY/GOLD AESTHETIC ---
const PRIMARY_ACCENT_COLOR = 'text-[#A98C6A]'; // Rich Tan/Gold
const BUTTON_BG_COLOR = 'bg-[#A98C6A]';
const HOVER_ACCENT_COLOR = 'hover:bg-[#8C755D]'; // Darker gold for buttons
const LIGHT_HOVER_ACCENT_COLOR = 'hover:bg-amber-50'; // Light gold hover for links
const BORDER_COLOR = 'border-[#A98C6A]';

const BG_COLOR = 'bg-gray-50'; // Light background for professionalism
const TEXT_COLOR_PRIMARY = 'text-gray-900';
const TEXT_COLOR_SECONDARY = 'text-gray-600';

// --- Utility Components ---

const Button = ({ children, onClick, primary = true, icon: Icon, className = '', type = 'button', disabled = false }) => (
  <button
    type={type}
    onClick={onClick}
    disabled={disabled}
    className={`
      flex items-center justify-center space-x-2 px-6 py-3 rounded-lg transition duration-300 shadow-md font-semibold text-sm
      ${primary 
        ? `${BUTTON_BG_COLOR} text-white ${HOVER_ACCENT_COLOR}` 
        : `bg-white ${PRIMARY_ACCENT_COLOR} border ${BORDER_COLOR} ${LIGHT_HOVER_ACCENT_COLOR}`
      }
      ${className}
      ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
    `}
  >
    {Icon && <Icon size={20} />}
    <span>{children}</span>
  </button>
);

const Card = ({ children, className = '' }) => (
    <div className={`p-6 bg-white rounded-lg shadow-lg border border-gray-200 ${className}`}>
        {children}
    </div>
);

// --- Page Components ---

const HomePage = ({ setCurrentPage }) => (
  <div className="space-y-16">
    {/* Hero Section - Matching the Image Content */}
    <div className="container mx-auto py-24 px-4 flex flex-col md:flex-row items-center justify-between gap-12">
        
        {/* Left Side: Text and CTA */}
        <div className="md:w-1/2 text-center md:text-left">
            <p className={`text-3xl font-extrabold ${TEXT_COLOR_PRIMARY} mb-2`}>Silvia Munjal</p>
            <h1 className={`text-4xl md:text-5xl font-extrabold ${PRIMARY_ACCENT_COLOR} leading-tight mb-4`}>
                International Business & Trade Lawyer
            </h1>
            <p className={`text-xl font-serif italic ${PRIMARY_ACCENT_COLOR} mb-6`}>
                "Securing Global Business, One Contract at a Time."
            </p>
            
            <p className={`mt-6 text-lg ${TEXT_COLOR_SECONDARY} max-w-xl md:max-w-none`}>
                Silvia Munjal is a trusted **International Business Lawyer** specializing in export & trade contracts, compliance, and cross-border dispute resolution. With over **500 contracts executed across 7+ countries**, she helps Indian businesses expand globally with confidence.
            </p>

            {/* CTA Button */}
            <div className="mt-10">
                <Button onClick={() => setCurrentPage('Contact')} icon={MessageSquare} className="py-4 px-8 text-base">
                    Book a Consultation Call
                </Button>
            </div>
        </div>

        {/* Right Side: Image Placeholder */}
        <div className="md:w-1/2 flex justify-center md:justify-end">
            <div className="w-80 h-80 rounded-full overflow-hidden shadow-2xl border-4 border-[#A98C6A]">
                {/*  */}
                <img 
                    src="https://placehold.co/800x800/A98C6A/FFFFFF?text=Silvia+Munjal+Advocate" 
                    alt="Silvia Munjal, International Business Lawyer" 
                    className="w-full h-full object-cover"
                    onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/800x800/A98C6A/FFFFFF?text=Silvia+Munjal+Advocate" }}
                />
            </div>
        </div>
    </div>

    {/* Stats Section - Matching the Document Content */}
    <div className="bg-white py-12 border-t border-gray-200">
        <div className="container mx-auto px-4 flex justify-around text-center">
            <div className="w-1/3">
                <p className={`text-5xl font-extrabold ${PRIMARY_ACCENT_COLOR}`}>500+</p>
                <p className={`text-base font-semibold ${TEXT_COLOR_SECONDARY} uppercase tracking-wider mt-2`}>Contracts Drafted & Negotiated</p>
            </div>
            <div className="w-1/3">
                <p className={`text-5xl font-extrabold ${PRIMARY_ACCENT_COLOR}`}>7+</p>
                <p className={`text-base font-semibold ${TEXT_COLOR_SECONDARY} uppercase tracking-wider mt-2`}>Countries Served</p>
            </div>
            <div className="w-1/3">
                <p className={`text-5xl font-extrabold ${PRIMARY_ACCENT_COLOR}`}>30+</p>
                <p className={`text-base font-semibold ${TEXT_COLOR_SECONDARY} uppercase tracking-wider mt-2`}>Overseas Clients</p>
            </div>
        </div>
    </div>

    {/* Services Preview Section - Classy Layout */}
    <div className="container mx-auto px-4 py-16">
        <h2 className={`text-3xl font-bold ${TEXT_COLOR_PRIMARY} mb-10 text-center`}>Specialized Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center">
                <Globe size={32} className={`${PRIMARY_ACCENT_COLOR} mx-auto`} />
                <h3 className={`text-xl font-bold mt-4 ${TEXT_COLOR_PRIMARY}`}>Export & Trade Contracts</h3>
                <p className={`mt-2 text-sm ${TEXT_COLOR_SECONDARY}`}>Legally sound agreements for global trade and distribution channels.</p>
            </Card>
            <Card className="text-center">
                <FileCheck size={32} className={`${PRIMARY_ACCENT_COLOR} mx-auto`} />
                <h3 className={`text-xl font-bold mt-4 ${TEXT_COLOR_PRIMARY}`}>Compliance & Regulatory</h3>
                <p className={`mt-2 text-sm ${TEXT_COLOR_SECONDARY}`}>Advisory for cross-border regulations, customs, and global legal frameworks.</p>
            </Card>
            <Card className="text-center">
                <DollarSign size={32} className={`${PRIMARY_ACCENT_COLOR} mx-auto`} />
                <h3 className={`text-xl font-bold mt-4 ${TEXT_COLOR_PRIMARY}`}>Risk & Dispute Resolution</h3>
                <p className={`mt-2 text-sm ${TEXT_COLOR_SECONDARY}`}>Protecting businesses from costly disputes through proactive risk management and mediation.</p>
            </Card>
            <Card className="text-center">
                <Briefcase size={32} className={`${PRIMARY_ACCENT_COLOR} mx-auto`} />
                <h3 className={`text-xl font-bold mt-4 ${TEXT_COLOR_PRIMARY}`}>Business Negotiations</h3>
                <p className={`mt-2 text-sm ${TEXT_COLOR_SECONDARY}`}>Securing favorable, long-term terms for international partnerships and ventures.</p>
            </Card>
        </div>
        <div className="mt-12 text-center">
            <Button primary={false} onClick={() => setCurrentPage('PracticeAreas')} icon={ChevronRight}>Learn More About Services</Button>
        </div>
    </div>
  </div>
);

const PublicationsPage = () => {
    const [selectedArea, setSelectedArea] = useState('All');
    
    // Simulate fetching content (would hit /api/publications in reality)
    const filteredPublications = DUMMY_PUBLICATIONS.filter(p => selectedArea === 'All' || p.area === selectedArea);

    return (
        <div className="container mx-auto py-16 px-4">
            <h1 className={`text-4xl font-bold ${TEXT_COLOR_PRIMARY} mb-2`}>Publications & Thought Leadership</h1>
            <p className={`text-xl ${TEXT_COLOR_SECONDARY} mb-8`}>Access professional analysis and articles on recent legal developments.</p>
            
            {/* Filter Section (Requirement 2: Filterable) */}
            <div className="mb-8 flex flex-wrap gap-3 items-center">
                <span className={`font-medium ${TEXT_COLOR_PRIMARY} self-center mr-2 text-sm uppercase`}>Filter:</span>
                <button
                    onClick={() => setSelectedArea('All')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition shadow-sm 
                        ${selectedArea === 'All' ? `${BUTTON_BG_COLOR} text-white` : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-100'}`}
                >
                    All Areas
                </button>
                {PRACTICE_AREAS.map(area => (
                    <button
                        key={area}
                        onClick={() => setSelectedArea(area)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition shadow-sm 
                            ${selectedArea === area ? `${BUTTON_BG_COLOR} text-white` : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-100'}`}
                    >
                        {area}
                    </button>
                ))}
            </div>

            {/* List of Publications */}
            <div className="space-y-6">
                {filteredPublications.map(pub => (
                    <Card key={pub.id} className="hover:ring-1 hover:ring-[#A98C6A] transition duration-300">
                        <div className="flex justify-between items-start">
                            <h2 className={`text-xl font-bold ${PRIMARY_ACCENT_COLOR}`}>{pub.title}</h2>
                            <span className="text-xs font-semibold text-gray-500 bg-gray-100 px-3 py-1 rounded-full">{pub.date}</span>
                        </div>
                        <p className={`text-sm ${TEXT_COLOR_SECONDARY} mt-1`}>{pub.area}</p>
                        <p className={`mt-3 ${TEXT_COLOR_SECONDARY}`}>{pub.summary}</p>
                        <a href={pub.link} className={`mt-3 inline-flex items-center text-sm font-semibold ${PRIMARY_ACCENT_COLOR} hover:${TEXT_COLOR_PRIMARY} transition`}>
                            Read Full Article <ChevronRight size={16} className="ml-1" />
                        </a>
                    </Card>
                ))}
                 {filteredPublications.length === 0 && (
                    <p className="text-gray-500 italic mt-8">No publications found for the selected area.</p>
                )}
            </div>
        </div>
    );
};

const AIAssistant = () => {
    const [query, setQuery] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    // Simulate the FastAPI /api/qa-chatbot endpoint (Requirement 6)
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        const userMessage = { sender: 'user', text: query, id: Date.now() };
        setChatHistory(prev => [...prev, userMessage]);
        setQuery('');
        setIsLoading(true);

        // Simulated RAG response based on legal context
        const dummyResponses = [
            "Based on the firm's indexed publications, the advocate has advised on cross-border e-commerce contracts focusing on jurisdiction and payment dispute clauses. A publication from Sep 2025 covers risk mitigation strategies.",
            "I found a Case Study relating to corporate compliance. It details a successful resolution using mediation under SIAC rules, as described in the firm's approach to Alternative Dispute Resolution.",
            "The firm's expertise includes navigating post-Brexit trade compliance. A publication from Oct 2025 outlines the new documentation and tariff requirements for UK exports.",
            "I apologize, but I cannot provide an answer based on the firm's documented knowledge base for that specific subject. Please use the contact form for a personal consultation."
        ];
        
        const delay = Math.random() * 1500 + 1000; // Simulate AI processing time (1s to 2.5s)
        
        setTimeout(() => {
            const aiResponseText = dummyResponses[Math.floor(Math.random() * dummyResponses.length)];
            const aiMessage = { sender: 'ai', text: aiResponseText, id: Date.now() + 1 };
            setChatHistory(prev => [...prev, aiMessage]);
            setIsLoading(false);
        }, delay);
    };

    return (
        <div className="container mx-auto py-16 px-4 max-w-3xl">
            <h1 className={`text-4xl font-bold ${TEXT_COLOR_PRIMARY} mb-2`}>AI Knowledge Assistant</h1>
            <p className={`text-lg ${TEXT_COLOR_SECONDARY} mb-8`}>Ask questions about our practice areas, publications, or general legal FAQs. **This simulates the RAG chatbot powered by the FastAPI LLM endpoint.**</p>

            <Card className="h-[60vh] flex flex-col">
                {/* Chat History */}
                <div className="flex-grow overflow-y-auto space-y-4 p-4 mb-4 border-b border-gray-200">
                    {chatHistory.length === 0 && (
                        <p className="text-center text-gray-400 mt-16 text-sm flex items-center justify-center">
                            <Search size={16} className="mr-2" /> Type a query to search the firm's indexed knowledge base.
                        </p>
                    )}
                    {chatHistory.map(msg => (
                        <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-xs md:max-w-md p-3 rounded-xl shadow-sm ${msg.sender === 'user' ? `${BUTTON_BG_COLOR} text-white rounded-br-none` : 'bg-gray-100 text-gray-800 rounded-tl-none'}`}>
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                             <div className="max-w-md p-3 rounded-xl bg-gray-100 text-gray-600 rounded-tl-none animate-pulse">
                                AI Assistant is processing...
                            </div>
                        </div>
                    )}
                </div>

                {/* Input Form */}
                <form onSubmit={handleSubmit} className="flex space-x-3 p-4">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Ask a question..."
                        disabled={isLoading}
                        className="flex-grow border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-[#A98C6A] focus:border-transparent transition"
                    />
                    <Button type="submit" primary={true} disabled={isLoading} icon={ChevronRight}>
                        Ask
                    </Button>
                </form>
            </Card>
        </div>
    );
};

const SecurePortal = ({ setIsLoggedIn, isLoggedIn }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [uploadStep, setUploadStep] = useState(1);
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState(null);

    const handleLogin = (e) => {
        e.preventDefault();
        // Simulate successful FastAPI /auth/login call
        if (email === 'client@test.com' && password === 'password') {
            setIsLoggedIn(true);
        } else {
            // In a real app, you would display a discreet error message
            alert("Simulated: Login failed. Use 'client@test.com' / 'password'");
        }
    };

    const handleFileUpload = (e) => {
        e.preventDefault();
        if (!file) return;
        
        setUploadStatus('Uploading...');
        // Simulate API /portal/documents/upload call with 1s network delay
        setTimeout(() => {
            setUploadStatus('Analyzing...');
            // In reality, the FastAPI backend initiates the LLM Summary job here.
            setTimeout(() => {
                setUploadStatus('Complete');
                setUploadStep(3); 
            }, 3000); // Simulate LLM processing delay
        }, 1000); 
    };

    if (!isLoggedIn) {
        return (
            <div className="container mx-auto py-20 px-4 max-w-lg">
                <Card>
                    <h1 className={`text-3xl font-bold ${TEXT_COLOR_PRIMARY} mb-6 text-center`}>Secure Client Login</h1>
                    <form onSubmit={handleLogin} className="space-y-4">
                        <input
                            type="email"
                            placeholder="Email (client@test.com)"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-[#A98C6A]"
                            required
                        />
                        {/* BUG FIX: Correctly setting password state */}
                        <input
                            type="password"
                            placeholder="Password (password)"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)} 
                            className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-[#A98C6A]"
                            required
                        />
                        <Button type="submit" className="w-full" icon={Lock}>
                            Access Portal
                        </Button>
                    </form>
                    <p className={`mt-4 text-center text-sm ${TEXT_COLOR_SECONDARY}`}>Demo Credentials: client@test.com / password</p>
                </Card>
            </div>
        );
    }

    // --- Secured Portal Dashboard (Requirement 1 & 4) ---
    return (
        <div className="container mx-auto py-16 px-4">
            <h1 className={`text-4xl font-bold ${TEXT_COLOR_PRIMARY} mb-2 flex items-center`}>
                <Lock size={30} className="mr-2 text-red-600" /> Client Document Portal
            </h1>
            <p className={`text-lg ${TEXT_COLOR_SECONDARY} mb-8`}>Welcome back, client@test.com. This is a private, authenticated workspace.</p>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* 1. Document Upload Utility */}
                <Card className={`lg:col-span-1 border-4 border-dashed border-[#A98C6A] p-6 h-fit`}>
                    <h2 className={`text-2xl font-bold mb-4 flex items-center ${TEXT_COLOR_PRIMARY}`}><Upload size={24} className="mr-2" /> Secure Document Upload</h2>
                    
                    {uploadStep === 1 && (
                        <div className="space-y-4">
                            <input 
                                type="file" 
                                onChange={(e) => setFile(e.target.files[0])}
                                className="w-full p-2 border border-gray-300 rounded-lg"
                            />
                            <Button 
                                onClick={() => file && setUploadStep(2)} 
                                primary={true}
                                disabled={!file}
                                className="w-full"
                                icon={ChevronRight}
                            >
                                Next: Review
                            </Button>
                            {file && <p className={`text-sm ${TEXT_COLOR_SECONDARY}`}>File selected: {file.name}</p>}
                        </div>
                    )}
                    
                    {uploadStep === 2 && (
                        <div className="space-y-4">
                            <p className="font-semibold">Confirm Upload:</p>
                            <p className={`text-sm ${TEXT_COLOR_SECONDARY}`}>File: {file?.name}</p>
                            <p className={`text-sm ${TEXT_COLOR_SECONDARY}`}>Size: {(file?.size / 1024).toFixed(2)} KB</p>
                            <Button 
                                onClick={handleFileUpload} 
                                disabled={uploadStatus === 'Uploading...' || uploadStatus === 'Analyzing...'} 
                                className="w-full"
                                icon={uploadStatus === 'Complete' ? CheckCircle : Upload}
                            >
                                {uploadStatus === 'Complete' ? 'Upload Done!' : (uploadStatus || 'Start Upload & Analysis')}
                            </Button>
                             {uploadStatus && <p className="text-center text-sm mt-3 text-red-600 font-medium">Simulated: FastAPI uploads to S3 and triggers LLM summary job.</p>}
                        </div>
                    )}

                    {uploadStep === 3 && (
                        <div className="text-center space-y-4">
                            <CheckCircle size={48} className="text-green-500 mx-auto" />
                            <h3 className={`text-xl font-bold ${TEXT_COLOR_PRIMARY}`}>Upload Successful!</h3>
                            <p className={`text-gray-600`}>The document is now awaiting review. The AI summary is available in the list.</p>
                            <Button onClick={() => { setUploadStep(1); setFile(null); setUploadStatus(null); }}>
                                Upload Another Document
                            </Button>
                        </div>
                    )}
                </Card>

                {/* 2. Document List (LLM Summary Display) */}
                <div className="lg:col-span-2 space-y-6">
                    <h2 className={`text-2xl font-bold ${TEXT_COLOR_PRIMARY} mb-4 flex items-center`}><FileText size={24} className="mr-2" /> Your Documents</h2>
                    {DUMMY_DOCUMENTS.map(doc => (
                        <Card key={doc.id} className="p-5">
                            <div className="flex justify-between items-center">
                                <h3 className={`text-lg font-bold ${PRIMARY_ACCENT_COLOR}`}>{doc.name}</h3>
                                <span className={`text-sm font-semibold px-3 py-1 rounded-full ${doc.status === 'Reviewed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                                    {doc.status}
                                </span>
                            </div>
                            <p className={`text-xs ${TEXT_COLOR_SECONDARY} mt-1`}>Uploaded: {doc.date}</p>
                            
                            <div className="mt-4 p-3 bg-gray-50 border-l-4 border-gray-300 rounded-r-lg">
                                <p className={`font-semibold text-sm ${TEXT_COLOR_PRIMARY} mb-1`}>AI Document Summary (LLM Output):</p>
                                <p className={`text-sm ${TEXT_COLOR_SECONDARY} italic`}>{doc.summary}</p>
                            </div>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
};


// --- Main Application Component ---
const App = () => {
  const [currentPage, setCurrentPage] = useState('Home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'Home':
        return <HomePage setCurrentPage={setCurrentPage} />;
      case 'PracticeAreas':
        return <PublicationsPage />; 
      case 'Publications':
        return <PublicationsPage />;
      case 'Contact':
        return <AIAssistant />; 
      case 'Portal':
        return <SecurePortal isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />;
      default:
        return <HomePage setCurrentPage={setCurrentPage} />;
    }
  };

  const NavItem = ({ name, page }) => (
    <button
      onClick={() => {
        setCurrentPage(page);
        setIsMobileMenuOpen(false); 
      }}
      className={`px-4 py-2 font-medium transition duration-200 rounded-lg 
        ${currentPage === page 
          ? `${PRIMARY_ACCENT_COLOR} border-b-2 border-[#A98C6A] ${TEXT_COLOR_PRIMARY}` 
          : `${TEXT_COLOR_SECONDARY} hover:${TEXT_COLOR_PRIMARY} hover:bg-gray-100`
        }`}
    >
      {name}
    </button>
  );

  return (
    <div className={`min-h-screen font-sans ${BG_COLOR}`}>
      {/* Header and Navigation */}
      <header className="bg-white shadow-lg sticky top-0 z-20">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          {/* Logo/Name */}
          <div className={`text-2xl font-extrabold ${TEXT_COLOR_PRIMARY}`}>
            <span className={PRIMARY_ACCENT_COLOR}>Silvia</span> Munjal
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex space-x-2">
            <NavItem name="Home" page="Home" />
            <NavItem name="Practice Areas" page="PracticeAreas" />
            <NavItem name="Publications" page="Publications" />
            <NavItem name="AI Assistant (Q&A)" page="Contact" />
            <NavItem name="Secure Portal" page="Portal" />
          </nav>
          
          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button primary={false} icon={isMobileMenuOpen ? X : Menu} onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
              Menu
            </Button>
          </div>
        </div>

        {/* Mobile Menu Overlay */}
        {isMobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-white shadow-lg py-4 border-t border-gray-200">
            <nav className="flex flex-col items-center space-y-3">
              <NavItem name="Home" page="Home" />
              <NavItem name="Practice Areas" page="PracticeAreas" />
              <NavItem name="Publications" page="Publications" />
              <NavItem name="AI Assistant (Q&A)" page="Contact" />
              <NavItem name="Secure Portal" page="Portal" />
            </nav>
          </div>
        )}
      </header>

      <main>
        {renderPage()}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12 py-10">
          <div className="container mx-auto px-4 text-center">
              <p className="text-lg font-semibold mb-2">Silvia Munjal, Advocate</p>
              <p className="text-sm text-gray-400">Built with React, Tailwind CSS, and a FastAPI/Python AI Backend.</p>
              <p className="text-xs text-gray-500 mt-2">Copyright © 2025. All Rights Reserved.</p>
          </div>
      </footer>
    </div>
  );
};

export default App;
