# ABSCO All Building Services Company - Website PRD

## Original Problem Statement
Build a professional website for ABSCO ALL BUILDING SERVICES COMPANY, a cleaning/building services company in Los Angeles, CA. Features: hamburger menu, WhatsApp button, before/after gallery, Apple-level animations, contact form with real email (Resend), SEO optimization.

## Architecture
- **Frontend**: React + Tailwind CSS + shadcn/ui + Framer Motion
- **Backend**: FastAPI + MongoDB + Resend email
- **Design**: Dark luxury theme (deep purple/blue palette)

## User Personas
- Business owners in LA needing cleaning services
- Property managers seeking maintenance contractors
- Residential clients looking for floor cleaning

## Core Requirements (Static)
- Single-page marketing website
- Mobile-responsive with hamburger menu
- Floating WhatsApp button (+502 55964028)
- Before/After gallery (25 images, 3 videos)
- Contact form sending real emails via Resend
- SEO optimized for LA cleaning services
- Company info: 1162 E. 42nd Street, LA, CA 90011-3109

## What's Been Implemented (March 2026)
- Full single-page website with 6 sections: Hero, Services, About, Gallery, Contact, Footer
- Navigation with mobile hamburger menu
- Floating WhatsApp button with pulse animation
- Before/After slider gallery with Photos/Videos tabs
- Contact form integrated with Resend email API
- SEO meta tags + JSON-LD structured data
- Dark theme with purple/blue/white color palette
- Framer Motion animations throughout
- Backend POST /api/contact endpoint

## P0 (Critical) - DONE
- [x] All sections built and functional
- [x] Contact form sends real emails
- [x] Mobile responsive
- [x] WhatsApp button
- [x] SEO tags

## P1 (Important) - Backlog
- [ ] Replace placeholder images with user's 25 real images + 3 videos
- [ ] Domain verification for Resend (to send to any email)
- [ ] Google Analytics integration
- [ ] Loading animation/skeleton

## P2 (Nice to Have)
- [ ] Testimonials section
- [ ] Blog/News section
- [ ] Multi-language (English/Spanish)
- [ ] Service area map
