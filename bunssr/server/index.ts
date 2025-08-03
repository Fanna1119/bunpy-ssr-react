/// <reference types="bun-types" />
import path from "path";
import { createElement } from "react";
import { renderToString } from "react-dom/server";

const socketPath = process.env.BUN_RENDER_SOCKET || "/tmp/bun_render_socket";

const handleRequest = async (data: string) => {
  try {
    const parsedData = JSON.parse(data);
    const { componentPath, props } = parsedData;

    if (!componentPath) {
      return JSON.stringify({ error: "Component path is required" });
    }

    const resolvedPath = path.resolve(componentPath);

    const componentModule = await import(resolvedPath);
    const Component = componentModule.default;

    if (!Component) {
      throw new Error(`No default export found in ${resolvedPath}`);
    }

    // Standard React render to string
    const html = renderToString(createElement(Component, props));

    return JSON.stringify({ html });
  } catch (error) {
    return JSON.stringify({ error: error.message });
  }
};

Bun.serve({
  unix: socketPath,
  async fetch(req) {
    const component_data = await req.text();
    const response = await handleRequest(component_data);
    return new Response(response, {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  },
});
