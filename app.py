<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>AdPlatform — Standalone</title>

  <!-- Tailwind (CDN) -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- React (UMD) -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>

  <!-- Babel for JSX in-browser (development) -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <style>
    /* Small helper to limit monospace block width on mobile */
    pre { white-space: pre-wrap; word-break: break-word; }
  </style>
</head>
<body class="antialiased bg-gray-50">

  <div id="root"></div>

  <!-- App code -->
  <script type="text/babel">

    const { useState, useEffect, useCallback } = React;

    /* -------------------------
       Simple Icon components
       ------------------------- */
    const Icon = ({children, className="", size=20}) => (
      <span className={`inline-flex items-center justify-center ${className}`} style={{width:size, height:size}}>
        {children}
      </span>
    );
    const Icons = {
      Dashboard: (props) => <Icon {...props}>📊</Icon>,
      Dollar: (props)=> <Icon {...props}>💲</Icon>,
      Zap: (props)=> <Icon {...props}>⚡</Icon>,
      Eye: (props)=> <Icon {...props}>👁️</Icon>,
      Plus: (props)=> <Icon {...props}>➕</Icon>,
      Code: (props)=> <Icon {...props}>⎋</Icon>,
      Trash: (props)=> <Icon {...props}>🗑️</Icon>,
      Loader: (props)=> <Icon {...props}>⏳</Icon>,
      User: (props)=> <Icon {...props}>👤</Icon>,
      Wallet: (props)=> <Icon {...props}>👛</Icon>,
      Share: (props)=> <Icon {...props}>🔗</Icon>,
      Menu: (props)=> <Icon {...props}>☰</Icon>,
      Chart: (props)=> <Icon {...props}>📈</Icon>,
      Link: (props)=> <Icon {...props}>🔗</Icon>,
      Light: (props)=> <Icon {...props}>💡</Icon>,
      Star: (props)=> <Icon {...props}>⭐</Icon>,
      Help: (props)=> <Icon {...props}>❓</Icon>,
      Send: (props)=> <Icon {...props}>📤</Icon>,
      Credit: (props)=> <Icon {...props}>💳</Icon>,
      X: (props)=> <Icon {...props}>✖</Icon>,
    };

    /* -------------------------
       Mock data + simple storage
       ------------------------- */
    const defaultMockKpis = [
      { id:1, name:'Total Revenue', value:'$1,250.34', icon:Icons.Dollar, color:'text-green-600', description:'Last 30 days earnings' },
      { id:2, name:'eCPM', value:'$4.21', icon:Icons.Zap, color:'text-yellow-500', description:'Effective Cost Per Mille' },
      { id:3, name:'Impressions', value:'297,058', icon:Icons.Eye, color:'text-blue-500', description:'Ads shown to users' },
      { id:4, name:'Affiliate Commission', value:'$52.90', icon:Icons.Share, color:'text-pink-500', description:'Earnings from referrals' },
    ];

    const STORAGE_KEY = 'adplatform_demo_state_v1';

    function loadState() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return null;
        return JSON.parse(raw);
      } catch(e) {
        console.error('loadState parse error', e);
        return null;
      }
    }
    function saveState(state) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch(e) {
        console.error('saveState error', e);
      }
    }

    /* -------------------------
       Small reusable UI
       ------------------------- */
    const CustomModal = ({title, children, onClose}) => (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-60 p-4">
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg">
          <div className="flex justify-between items-center p-5 border-b">
            <h3 className="text-lg font-semibold">{title}</h3>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700 p-2">
              <Icons.X />
            </button>
          </div>
          <div className="p-6">{children}</div>
        </div>
      </div>
    );

    const MetricCard = ({kpi}) => {
      const IconComp = kpi.icon;
      return (
        <div className="bg-white p-5 rounded-xl shadow border-l-4 border-indigo-500 transform hover:scale-[1.02] transition">
          <div className="flex items-center">
            <div className={`p-3 rounded-full ${kpi.color} bg-opacity-10`}>
              <IconComp />
            </div>
            <div className="ml-4">
              <h4 className="text-xs font-semibold text-gray-500 uppercase">{kpi.name}</h4>
              <div className="text-2xl font-extrabold text-gray-900">{kpi.value}</div>
            </div>
          </div>
          <p className="mt-3 text-xs text-gray-400">{kpi.description}</p>
        </div>
      );
    };

    /* -------------------------
       Ad Unit Components
       ------------------------- */
    function AdUnitCard({unit, onDelete}) {
      const [showCode, setShowCode] = useState(false);
      const integrationCode = `<div data-ad-unit-id="${unit.id}" data-size="${unit.size}"></div>\n<script async src="https://monetize.example.com/ad-loader.js"></script>`;
      const copyToClipboard = () => {
        navigator.clipboard?.writeText(integrationCode).then(()=> {
          alert('Integration code copied!');
        }).catch(()=> {
          // fallback
          const ta = document.createElement('textarea');
          ta.value = integrationCode;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          alert('Integration code copied!');
        })
      };
      const statusClass = unit.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';

      return (
        <div className="bg-white p-4 rounded-xl shadow border">
          <div className="flex justify-between items-start mb-3">
            <div>
              <h3 className="text-lg font-bold text-gray-800">{unit.name}</h3>
              <p className={`text-xs inline-block mt-1 px-2 py-0.5 rounded-full ${statusClass}`}>{unit.status}</p>
            </div>
            <button onClick={()=> onDelete(unit.id)} className="text-red-500 hover:text-red-700 p-1">
              <Icons.Trash />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
            <div><span className="font-semibold text-gray-700">Size:</span> {unit.size}</div>
            <div><span className="font-semibold text-gray-700">eCPM Goal:</span> ${unit.eCPM_goal.toFixed(2)}</div>
            <div className="col-span-2"><span className="font-semibold text-gray-700">Created:</span> {new Date(unit.created_at).toLocaleDateString()}</div>
          </div>

          <div className="mt-4 border-t pt-4">
            <button onClick={() => setShowCode(s => !s)} className="text-indigo-600 text-sm font-medium flex items-center">
              <Icons.Code className="mr-2" /> {showCode ? 'Hide Integration Code' : 'Show Integration Code'}
            </button>
            {showCode && (
              <div className="mt-3 p-3 bg-gray-50 rounded text-xs font-mono relative">
                <pre>{integrationCode}</pre>
                <button onClick={copyToClipboard} className="absolute top-2 right-2 px-2 py-1 bg-indigo-600 text-white rounded text-xs">Copy</button>
              </div>
            )}
          </div>
        </div>
      );
    }

    function AddUnitForm({onAdd}) {
      const [name, setName] = useState('');
      const [size, setSize] = useState('300x250');
      const [eCPM, setECPM] = useState(5.00);
      const [busy, setBusy] = useState(false);
      const sizes = ['300x250','728x90','320x50','160x600'];

      const submit = async (e) => {
        e.preventDefault();
        if (!name) return alert('Enter a unit name');
        setBusy(true);
        try {
          await new Promise(r=>setTimeout(r, 200)); // mimic async
          onAdd({
            id: 'unit_' + Date.now(),
            name,
            size,
            eCPM_goal: Number(eCPM),
            status: 'Active',
            created_at: Date.now()
          });
          setName('');
          setSize('300x250');
          setECPM(5.00);
        } catch(err) {
          console.error(err);
          alert('Failed to add unit');
        } finally {
          setBusy(false);
        }
      };

      return (
        <div className="bg-white p-6 rounded-xl shadow border mt-6">
          <h3 className="text-xl font-bold text-indigo-700 mb-4 flex items-center"><Icons.Plus /> <span className="ml-2">Create New Ad Unit</span></h3>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700 block">Unit Name</label>
              <input value={name} onChange={e=>setName(e.target.value)} required placeholder="Homepage Footer" className="mt-1 w-full p-3 border rounded" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-700 block">Size</label>
                <select className="mt-1 w-full p-3 border rounded" value={sizes.find(s=>s===size)||size} onChange={e=>setSize(e.target.value)}>
                  {sizes.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 block">eCPM Goal ($)</label>
                <input type="number" min="0.01" step="0.01" value={eCPM} onChange={e=>setECPM(e.target.value)} className="mt-1 w-full p-3 border rounded"/>
              </div>
            </div>
            <button className="w-full py-3 bg-indigo-600 text-white rounded" disabled={busy}>
              {busy ? <><Icons.Loader/> Processing...</> : <> <Icons.Plus/> Add Unit</>}
            </button>
          </form>
        </div>
      );
    }

    /* -------------------------
       Payment / Wallet manager (mock)
       ------------------------- */
    function WalletManager({balance, onTopUp, onWithdraw}) {
      const [showTopUp, setShowTopUp] = useState(false);
      const [showWithdraw, setShowWithdraw] = useState(false);

      return (
        <div className="bg-white p-6 rounded-xl shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-500 uppercase">Available Funds</p>
              <div className="text-3xl font-extrabold text-purple-800">${balance.toFixed(2)}</div>
            </div>
            <div className="space-x-2">
              <button onClick={()=>setShowTopUp(true)} className="py-2 px-4 bg-green-500 text-white rounded">Top Up</button>
              <button onClick={()=>setShowWithdraw(true)} className="py-2 px-4 bg-red-500 text-white rounded">Withdraw</button>
            </div>
          </div>

          {showTopUp && (
            <CustomModal title="Top Up Wallet" onClose={()=>setShowTopUp(false)}>
              <WalletForm onSubmit={async (amt)=>{ await onTopUp(amt); setShowTopUp(false); }} />
            </CustomModal>
          )}
          {showWithdraw && (
            <CustomModal title="Withdraw Funds" onClose={()=>setShowWithdraw(false)}>
              <WalletForm isWithdraw currentBalance={balance} onSubmit={async (amt)=>{ await onWithdraw(amt); setShowWithdraw(false); }} />
            </CustomModal>
          )}
        </div>
      );
    }

    function WalletForm({isWithdraw=false, currentBalance=0, onSubmit}) {
      const [amount, setAmount] = useState(100.00);
      const [processing, setProcessing] = useState(false);
      const [error, setError] = useState(null);

      const submit = async (e) => {
        e.preventDefault();
        setError(null);
        if (amount <= 0) { setError('Enter positive amount'); return; }
        if (isWithdraw && amount > currentBalance) { setError('Insufficient funds'); return; }
        setProcessing(true);
        try {
          await new Promise(r=>setTimeout(r, 300));
          await onSubmit(Number(amount));
        } catch(err) {
          setError(err.message || 'Transaction failed');
        } finally { setProcessing(false); }
      };

      return (
        <form onSubmit={submit} className="space-y-4">
          <p className="text-sm text-gray-600">Available: <strong>${currentBalance.toFixed(2)}</strong></p>
          <div>
            <label className="text-sm text-gray-700 block">Amount ($)</label>
            <input type="number" step="0.01" min="0.01" value={amount} onChange={e=>setAmount(e.target.value)} className="mt-1 w-full p-3 border rounded text-lg font-bold"/>
          </div>
          {isWithdraw && <div className="text-xs p-2 bg-red-50 rounded">A 2% processing fee may apply.</div>}
          {error && <div className="text-sm text-red-600">{error}</div>}
          <div className="flex justify-end">
            <button className="py-2 px-4 bg-indigo-600 text-white rounded" disabled={processing}>{processing ? 'Processing...' : 'Submit'}</button>
          </div>
        </form>
      );
    }

    /* -------------------------
       Other small sections (Help / Insights / Websites)
       ------------------------- */
    const StatisticsPage = ({kpis}) => (
      <section>
        <div className="mb-6 flex items-center">
          <Icons.Chart /> <h2 className="ml-3 text-2xl font-bold">Performance Statistics</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {kpis.map(k=> <MetricCard key={k.id} kpi={k} />)}
        </div>

        <div className="mt-10">
          <h3 className="text-xl font-bold mb-3">Revenue Trend (Last 30 Days)</h3>
          <div className="bg-white rounded-xl p-6 h-64 flex items-center justify-center text-gray-400">[Chart placeholder — integrate chart library if needed]</div>
        </div>
      </section>
    );

    const WebsitesManager = () => (
      <section>
        <div className="mb-4 flex items-center"><Icons.Link /> <h3 className="ml-3 text-xl font-bold">Websites & Direct Link</h3></div>
        <div className="bg-white p-6 rounded-xl shadow border">
          <p className="text-gray-600">Manage sites where ad units are integrated</p>
          <ul className="mt-4 space-y-2">
            <li className="p-3 bg-gray-50 rounded flex justify-between"><span>monetize.example.com</span><span className="text-green-600">Verified</span></li>
            <li className="p-3 bg-gray-50 rounded flex justify-between"><span>new-project.io</span><span className="text-yellow-600">Pending</span></li>
          </ul>
        </div>
      </section>
    );

    const InsightsPage = () => (
      <section>
        <div className="mb-4 flex items-center"><Icons.Light /> <h3 className="ml-3 text-xl font-bold">Insights</h3></div>
        <div className="bg-white p-6 rounded-xl shadow border">
          <ul className="space-y-3">
            <li className="p-3 bg-yellow-50 rounded border-l-4 border-yellow-500">
              <strong>High Priority:</strong> Increase eCPM Goal for certain units.
            </li>
            <li className="p-3 bg-blue-50 rounded border-l-4 border-blue-500">
              <strong>Test:</strong> Try 728x90 on mobile top for premium inventory.
            </li>
          </ul>
        </div>
      </section>
    );

    const PriorityProgram = () => (
      <section>
        <div className="mb-4 flex items-center"><Icons.Star /> <h3 className="ml-3 text-xl font-bold">Priority Program</h3></div>
        <div className="bg-indigo-50 p-6 rounded-xl">Unlock dedicated account management and premium campaigns.</div>
      </section>
    );

    const HelpCenter = () => (
      <section>
        <div className="mb-4 flex items-center"><Icons.Help /> <h3 className="ml-3 text-xl font-bold">Help Center</h3></div>
        <div className="bg-white p-6 rounded-xl">
          <ul className="space-y-2 text-indigo-600">
            <li><a href="#" className="hover:underline">FAQ: Getting Started</a></li>
            <li><a href="#" className="hover:underline">Contact Support</a></li>
            <li><a href="#" className="hover:underline">Ad Unit Integration Guide</a></li>
          </ul>
        </div>
      </section>
    );

    const AffiliateProgramManager = ({userId}) => {
      const code = userId ? userId.slice(0,8).toUpperCase() : 'USER0000';
      const link = `https://monetize.example.com/signup?ref=${code}`;
      return (
        <div className="bg-white p-6 rounded-xl shadow border">
          <h3 className="text-lg font-bold mb-3">Referral Program</h3>
          <p className="text-gray-600 mb-3">Share your link to earn commission.</p>
          <div className="flex gap-2">
            <input className="flex-1 p-2 border rounded font-mono" readOnly value={link}/>
            <button className="px-4 bg-pink-500 text-white rounded" onClick={()=>navigator.clipboard?.writeText(link)}>Copy</button>
          </div>
        </div>
      );
    };

    /* -------------------------
       Main App
       ------------------------- */
    function App() {
      const [selectedView, setSelectedView] = useState('dashboard');
      const [kpis, setKpis] = useState(defaultMockKpis);
      const [adUnits, setAdUnits] = useState([]);
      const [balance, setBalance] = useState(0.00);
      const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);
      const [user] = useState({ uid: 'demo_user_1234' });

      // load stored state on mount
      useEffect(()=> {
        const st = loadState();
        if (st) {
          setAdUnits(st.adUnits || []);
          setBalance(st.balance || 0);
          setKpis(st.kpis || defaultMockKpis);
        } else {
          // seed with one ad unit
          const seed = [{
            id: 'unit_seed_1',
            name: 'Homepage Footer',
            size: '300x250',
            eCPM_goal: 5.00,
            status: 'Active',
            created_at: Date.now() - 1000*60*60*24*7
          }];
          setAdUnits(seed);
          setBalance(12.34);
          saveState({adUnits: seed, balance:12.34, kpis: defaultMockKpis});
        }
      },[]);

      // persist on adUnits or balance change
      useEffect(()=> {
        saveState({adUnits, balance, kpis});
      }, [adUnits, balance, kpis]);

      const addUnit = (unit) => {
        setAdUnits(prev => [unit, ...prev]);
      };

      const deleteUnit = (id) => {
        if (!confirm('Delete this ad unit?')) return;
        setAdUnits(prev => prev.filter(u => u.id !== id));
      };

      const topUp = async (amt) => {
        setBalance(b => Number((b + amt).toFixed(2)));
      };
      const withdraw = async (amt) => {
        if (amt > balance) throw new Error('Insufficient funds');
        setBalance(b => Number((b - amt).toFixed(2)));
      };

      const navItems = [
        {id:'dashboard', label:'Dashboard', icon:Icons.Dashboard},
        {id:'ad_units', label:'Ad Units', icon:Icons.Code},
        {id:'websites', label:'Websites', icon:Icons.Link},
        {id:'payments', label:'Payments', icon:Icons.Credit},
        {id:'insights', label:'Insights', icon:Icons.Light},
        {id:'referral', label:'Referral', icon:Icons.Share},
        {id:'priority', label:'Priority', icon:Icons.Star},
        {id:'help', label:'Help', icon:Icons.Help},
      ];

      function renderContent() {
        switch(selectedView) {
          case 'dashboard': return <StatisticsPage kpis={kpis} />;
          case 'ad_units': return (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">Your Ad Units ({adUnits.length})</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6"
print("Backend running...")
