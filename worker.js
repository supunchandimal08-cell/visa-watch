export default {
  async fetch(request, env) {
    // Serve the checked-in static dashboard and JSON assets through the
    // Cloudflare Workers Static Assets binding.
    return env.ASSETS.fetch(request);
  }
};
