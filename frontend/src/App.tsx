import { Route, Routes, Navigate } from "react-router";
import AppShell from "./components/AppShell";
import RouteGuard from "./components/RouteGuard";
import { BackendReadinessProvider } from "./lib/backendReadiness";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProjectCreate from "./pages/ProjectCreate";
import ProjectDetail from "./pages/ProjectDetail";
import ProjectEdit from "./pages/ProjectEdit";
import ProjectList from "./pages/ProjectList";

function App() {
  return (
    <BackendReadinessProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <RouteGuard>
              <AppShell>
                <Navigate to="/projects" replace />
              </AppShell>
            </RouteGuard>
          }
        />
        <Route
          path="/projects"
          element={
            <RouteGuard>
              <AppShell>
                <ProjectList />
              </AppShell>
            </RouteGuard>
          }
        />
        <Route
          path="/projects/new"
          element={
            <RouteGuard>
              <AppShell>
                <ProjectCreate />
              </AppShell>
            </RouteGuard>
          }
        />
        <Route
          path="/projects/:id"
          element={
            <RouteGuard>
              <AppShell>
                <ProjectDetail />
              </AppShell>
            </RouteGuard>
          }
        />
        <Route
          path="/projects/:id/edit"
          element={
            <RouteGuard>
              <AppShell>
                <ProjectEdit />
              </AppShell>
            </RouteGuard>
          }
        />
      </Routes>
    </BackendReadinessProvider>
  );
}

export default App;
