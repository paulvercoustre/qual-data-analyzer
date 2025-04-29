import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import './App.css';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';

// --- Project API Base URL (Consider moving to a config file) ---
const API_BASE_URL = 'http://localhost:8000'; // Adjust if your backend runs elsewhere

function Home() {
  const { isAuthenticated, logout, authToken } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);

  // --- State for New Project Form ---
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [createError, setCreateError] = useState(null);

  // --- Fetch Projects ---
  useEffect(() => {
    if (isAuthenticated) {
      const fetchProjects = async () => {
        setIsLoading(true);
        setFetchError(null);
        try {
          const response = await fetch(`${API_BASE_URL}/projects/`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${authToken}`,
              'Content-Type': 'application/json',
            },
          });
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch projects' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setProjects(data);
        } catch (err) {
          console.error("Fetch Projects Error:", err);
          setFetchError(err.message || 'An error occurred while fetching projects.');
        } finally {
          setIsLoading(false);
        }
      };

      fetchProjects();
    } else {
      // Clear projects if user logs out
      setProjects([]);
    }
  }, [isAuthenticated, authToken]); // Re-run effect if auth state changes

  // --- Handle New Project Submission ---
  const handleCreateProject = async (event) => {
    event.preventDefault();
    if (!newProjectName.trim()) {
      setCreateError('Project name cannot be empty.');
      return;
    }
    setIsCreating(true);
    setCreateError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newProjectName, description: newProjectDesc }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to create project' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      const createdProject = await response.json();
      setProjects(prevProjects => [createdProject, ...prevProjects]);
      setNewProjectName('');
      setNewProjectDesc('');
    } catch (err) {
      console.error("Create Project Error:", err);
      setCreateError(err.message || 'An error occurred while creating the project.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // --- Render Logic ---
  return (
    <div>
      <h1>Welcome to the QDAS App</h1>
      <nav>
        {!isAuthenticated ? (
          <>
            <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
          </>
        ) : (
          <button onClick={handleLogout}>Logout</button>
        )}
      </nav>

      {/* Conditional rendering for authenticated users */}
      {isAuthenticated && (
        <div className="dashboard">
          <h2>Your Projects</h2>

          {/* --- New Project Form --- */}
          <form onSubmit={handleCreateProject} className="new-project-form">
             <h3>Create New Project</h3>
             {createError && <p style={{ color: 'red' }}>Error: {createError}</p>}
             <div>
               <label htmlFor="projectName">Name:</label>
               <input
                 type="text"
                 id="projectName"
                 value={newProjectName}
                 onChange={(e) => setNewProjectName(e.target.value)}
                 required
                 disabled={isCreating}
               />
             </div>
             <div>
               <label htmlFor="projectDesc">Description (Optional):</label>
               <textarea
                 id="projectDesc"
                 value={newProjectDesc}
                 onChange={(e) => setNewProjectDesc(e.target.value)}
                 disabled={isCreating}
               />
             </div>
             <button type="submit" disabled={isCreating}>
               {isCreating ? 'Creating...' : 'Create Project'}
             </button>
          </form>
          {/* --- End New Project Form --- */}

          {/* --- Project List --- */}
          <h3>Existing Projects</h3>
          {isLoading && <p>Loading projects...</p>}
          {fetchError && <p style={{ color: 'red' }}>Error: {fetchError}</p>}
          {!isLoading && !fetchError && (
            projects.length === 0 ? (
              <p>You have no projects yet.</p>
            ) : (
              <ul>
                {projects.map(project => (
                  <li key={project.id}>
                    {project.name} {project.description ? `- ${project.description}` : ''}
                    {/* Add links/buttons for project actions later */}
                  </li>
                ))}
              </ul>
            )
          )}
          {/* --- End Project List --- */}
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default App;
