import { useState } from 'react'
import {checkHealth, indexRepo} from "./api"
import type { IndexResponse } from "./api";
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  // const [count, setCount] = useState(0)

  const [status, setStatus] = useState<string>("not checked yet");
  const [statusError, setStatusError] = useState<string | null>(null);
  const [repoInfo, setRepoInfo] = useState<IndexResponse | null>(null);
  const [repoUrl, setRepoUrl] = useState<string>("");

  const [isIndexing, setIsIndexing] = useState<boolean>(false);
  const [indexError, setIndexError] = useState<string | null>(null);
  
  async function handleCheckBackend() {
    setStatusError(null);
    try {
      const data = await checkHealth();
      setStatus(data.status);
    }
    catch(err) {
      setStatusError(err instanceof Error ? err.message : "Unknown Error");
    }
  }

  async function handleIndexRepository() {
    setRepoInfo(null);
    setIndexError(null);
    setIsIndexing(true);

    try {
      const data = await indexRepo(repoUrl);
      setRepoInfo(data);
    }
    catch (err) {
      setIndexError( err instanceof Error ? err.message : "Unknown indexing error");
    }
    finally { setIsIndexing(false); }
  }

  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sanns-serif"}}>
      <h1>Codebase Search</h1>
      <p>Cohere-powered codebase search tool</p>

      <section style={{marginBottom: "2rem"}}>
        <button onClick={handleCheckBackend}>Check Backend</button>

        <p>Backend status: <strong>{status}</strong></p>

        {statusError && <p style={{color:"red"}}>{statusError}</p> }
      </section>

      <section style={{ marginBottom: "2rem"}}>
        <h2>Index GitHub Repository</h2>
        <input 
          value={repoUrl}
          onChange={(event) => setRepoUrl(event.target.value)}
          style={{ width: "500px", maxWidth:"100%", padding: "0.5rem"}}
        />
        <button
          onClick={handleIndexRepository}
          disabled={isIndexing}
          style={{ marginLeft:"0.5rem"}}
        >
          {isIndexing ? "Indexing.." : "Index Repository"}

        </button>

        {repoInfo && (
          <div style={{marginTop:"2rem"}}>
            <p>Repo Id: {repoInfo.repo_id}</p>
            <p>Files: {repoInfo.file_count}</p>
            <p>Chunks: {repoInfo.chunk_count}</p>
          </div>
        )}

        {indexError && <p style={{color:"red"}}>{indexError}</p> }

      </section>
    </main>
  )

  // return (
  //   <>
  //     <section id="center">
  //       <div className="hero">
  //         <img src={heroImg} className="base" width="170" height="179" alt="" />
  //         <img src={reactLogo} className="framework" alt="React logo" />
  //         <img src={viteLogo} className="vite" alt="Vite logo" />
  //       </div>
  //       <div>
  //         <h1>Get started</h1>
  //         <p>
  //           Edit <code>src/App.tsx</code> and save to test <code>HMR</code>
  //         </p>
  //       </div>
  //       <button
  //         type="button"
  //         className="counter"
  //         onClick={() => setCount((count) => count + 1)}
  //       >
  //         Count is {count}
  //       </button>
  //     </section>

  //     <div className="ticks"></div>

  //     <section id="next-steps">
  //       <div id="docs">
  //         <svg className="icon" role="presentation" aria-hidden="true">
  //           <use href="/icons.svg#documentation-icon"></use>
  //         </svg>
  //         <h2>Documentation</h2>
  //         <p>Your questions, answered</p>
  //         <ul>
  //           <li>
  //             <a href="https://vite.dev/" target="_blank">
  //               <img className="logo" src={viteLogo} alt="" />
  //               Explore Vite
  //             </a>
  //           </li>
  //           <li>
  //             <a href="https://react.dev/" target="_blank">
  //               <img className="button-icon" src={reactLogo} alt="" />
  //               Learn more
  //             </a>
  //           </li>
  //         </ul>
  //       </div>
  //       <div id="social">
  //         <svg className="icon" role="presentation" aria-hidden="true">
  //           <use href="/icons.svg#social-icon"></use>
  //         </svg>
  //         <h2>Connect with us</h2>
  //         <p>Join the Vite community</p>
  //         <ul>
  //           <li>
  //             <a href="https://github.com/vitejs/vite" target="_blank">
  //               <svg
  //                 className="button-icon"
  //                 role="presentation"
  //                 aria-hidden="true"
  //               >
  //                 <use href="/icons.svg#github-icon"></use>
  //               </svg>
  //               GitHub
  //             </a>
  //           </li>
  //           <li>
  //             <a href="https://chat.vite.dev/" target="_blank">
  //               <svg
  //                 className="button-icon"
  //                 role="presentation"
  //                 aria-hidden="true"
  //               >
  //                 <use href="/icons.svg#discord-icon"></use>
  //               </svg>
  //               Discord
  //             </a>
  //           </li>
  //           <li>
  //             <a href="https://x.com/vite_js" target="_blank">
  //               <svg
  //                 className="button-icon"
  //                 role="presentation"
  //                 aria-hidden="true"
  //               >
  //                 <use href="/icons.svg#x-icon"></use>
  //               </svg>
  //               X.com
  //             </a>
  //           </li>
  //           <li>
  //             <a href="https://bsky.app/profile/vite.dev" target="_blank">
  //               <svg
  //                 className="button-icon"
  //                 role="presentation"
  //                 aria-hidden="true"
  //               >
  //                 <use href="/icons.svg#bluesky-icon"></use>
  //               </svg>
  //               Bluesky
  //             </a>
  //           </li>
  //         </ul>
  //       </div>
  //     </section>

  //     <div className="ticks"></div>
  //     <section id="spacer"></section>
  //   </>
  // )
}

export default App
