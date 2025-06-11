const { app, BrowserWindow } = require('electron')
const { spawn } = require('child_process')
const path = require('path')

let backendProcess = null;

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  })

  // Load the React app. In a production build, this would be `file://.../build/index.html`
  // For development, load from Vite's dev server.
  win.loadURL('http://localhost:5173') // Adjust if your Vite dev server uses a different port
}

function startBackend() {
  const backendPath = path.join(__dirname, 'backend', 'app', 'main.py');
  // Assuming 'venv' is your virtual environment directory at the project root
  const pythonExecutable = path.join(__dirname, 'venv', 'bin', 'python'); 

  backendProcess = spawn(pythonExecutable, ['-m', 'uvicorn', 'backend.app.main:app', '--reload'], {
    cwd: __dirname, // Ensure the backend runs from the project root
    env: { ...process.env, PYTHONPATH: __dirname },
    stdio: 'inherit' // This pipes backend output to the Electron console
  });

  backendProcess.on('error', (err) => {
    console.error('Failed to start backend process:', err);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  startBackend();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (backendProcess) {
    backendProcess.kill(); // Ensure backend process is killed when Electron app quits
  }
}); 