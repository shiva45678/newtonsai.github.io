export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    return new Response(`daily.txdx.in worker is running`, { status: 200 });
  }
} satisfies ExportedHandler<Env>;
