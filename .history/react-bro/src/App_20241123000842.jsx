// src/App.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";
import routes from "./routeConfig";

const App = () => {
  return (
    <React.Suspense fallback={<div>Loading...</div>}>
      <Routes>
        {routes.map((route, index) => (
          <Route key={index} path={route.path} element={<route.element />} />
        ))}
      </Routes>
    </React.Suspense>
  );
};

export default App;
