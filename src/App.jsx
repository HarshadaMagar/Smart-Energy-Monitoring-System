import { useState } from "react";

function BoltIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M13.2 2.5 5.8 13h5.1l-.1 8.5 7.4-11.2h-5z" />
    </svg>
  );
}

function HomeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 11.2 12 3l9 8.2M5.5 9.7V21h13V9.7M9.5 21v-7h5v7" />
    </svg>
  );
}

function BuildingIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 21V7h10v14M14 11h6v10M8 11h2M8 15h2M8 19h2M17 15h1M17 18h1M2 21h20" />
    </svg>
  );
}

function ShieldIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3 19 6v5c0 4.8-3 8.2-7 10-4-1.8-7-5.2-7-10V6zM9 12l2 2 4-4" />
    </svg>
  );
}

function EmailIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 5h18v14H3zM3 7l9 7 9-7" />
    </svg>
  );
}

function LockIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 10V7a5 5 0 0 1 10 0v3M5 10h14v11H5z" />
    </svg>
  );
}

function EyeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6zM12 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6z" />
    </svg>
  );
}

function ArrowIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  );
}

const accounts = [
  {
    name: "Domestic",
    title: "Domestic User",
    description: "Monitor your home energy",
    icon: HomeIcon,
  },
  {
    name: "Enterprise",
    title: "Enterprise User",
    description: "Manage organizational usage",
    icon: BuildingIcon,
  },
  {
    name: "Administrator",
    title: "System Administrator",
    description: "Control systems and access",
    icon: ShieldIcon,
  },
];

export default function App() {
  const [selectedAccount, setSelectedAccount] = useState("Domestic");
  const [showPassword, setShowPassword] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
  }

  return (
    <>
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <header className="topbar">
        <a className="brand" href="#" aria-label="VoltWise home">
          <span className="brand-mark"><BoltIcon /></span>
          <span className="brand-copy">
            <span className="wordmark">VOLT<span>WISE</span></span>
            <span className="tagline">Monitor smarter. Consume better.</span>
          </span>
        </a>

        <div className="system-status" role="status">
          <span className="status-dot" />
          <span>Smart energy monitoring system</span>
        </div>
      </header>

      <main className="login-shell">
        <section className="intro" aria-labelledby="login-heading">
          <p className="eyebrow">Secure account access</p>
          <h1 id="login-heading">Welcome to <span>VoltWise</span></h1>
          <p className="subtitle">Select your account type to continue.</p>
        </section>

        <section className="login-card" aria-label="Sign in">
          <div className="account-picker" role="tablist" aria-label="Account type">
            {accounts.map((account) => {
              const Icon = account.icon;
              const active = selectedAccount === account.name;
              return (
                <button
                  className={`account-option${active ? " active" : ""}`}
                  type="button"
                  role="tab"
                  aria-selected={active}
                  aria-controls="auth-panel"
                  key={account.name}
                  onClick={() => setSelectedAccount(account.name)}
                >
                  <span className="account-icon"><Icon /></span>
                  <span className="account-copy">
                    <strong>{account.title}</strong>
                    <small>{account.description}</small>
                  </span>
                  <span className="account-arrow" aria-hidden="true">›</span>
                </button>
              );
            })}
          </div>

          <form className="auth-panel" id="auth-panel" onSubmit={handleSubmit}>
            <div className="form-heading">
              <div>
                <p className="form-label">{selectedAccount} account</p>
                <h2>Sign in</h2>
              </div>
              <span className="secure-badge">
                <LockIcon />
                Secure
              </span>
            </div>

            <label className="field">
              <span>Email address</span>
              <span className="input-wrap">
                <EmailIcon />
                <input type="email" name="email" autoComplete="email" placeholder="you@example.com" required />
              </span>
            </label>

            <label className="field">
              <span>Password</span>
              <span className="input-wrap">
                <LockIcon />
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  required
                />
                <button
                  className="password-toggle"
                  type="button"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  onClick={() => setShowPassword((visible) => !visible)}
                >
                  <EyeIcon />
                </button>
              </span>
            </label>

            <div className="form-options">
              <label className="remember">
                <input type="checkbox" name="remember" />
                <span>Remember me</span>
              </label>
              <a href="#">Forgot password?</a>
            </div>

            <button className="submit-button" type="submit">
              <span>Sign in</span>
              <ArrowIcon />
            </button>

            <p className="create-account">New to VoltWise? <a href="#">Create an account</a></p>
          </form>
        </section>
      </main>

      <footer>
        <span>© 2026 VoltWise</span>
        <nav aria-label="Footer">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Support</a>
        </nav>
      </footer>
    </>
  );
}
