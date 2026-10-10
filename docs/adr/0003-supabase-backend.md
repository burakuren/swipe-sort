# Supabase as the backend platform

The backend is **Supabase**: hosted Postgres (the PowerSync source, ADR-0002), Auth (Google, email, Apple),
Storage for photo files, Postgres functions and Edge Functions for server logic. One vendor covers every
backend need, it is PowerSync's best-documented integration (guides, demos, attachments example), and
lock-in stays low because it is plain Postgres and the whole platform is open source and self-hostable.

## Considered Options

- **Neon + separate auth (Better Auth / Clerk) + R2/S3 + Cloudflare Workers:** good Postgres, but three to
  four vendors to wire together and keep secure.
- **Self-hosted Postgres and services on a VPS:** cheapest in money, most expensive in operations for a solo
  founder.
- **Firebase, Convex:** not Postgres; ruled out by ADR-0002.

## Consequences

- Writes from PowerSync go through Postgres functions called over RPC (our write API), not direct table
  access: Supabase stops exposing `public` tables to the Data API by default (new projects since
  2026-05-30, existing projects from 2026-10-30).
- PowerSync connects to Postgres directly; Supabase direct connections are IPv6-only (PowerSync Cloud
  handles this; a self-hosted PowerSync needs IPv6 or Supabase's IPv4 add-on).
- Free projects pause after a week idle: fine for development, production needs Pro (from $25/month).
- Built-in auth email is not for production (about 2 messages/hour, team members only): custom SMTP needed.
