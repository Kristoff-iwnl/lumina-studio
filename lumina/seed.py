"""
Seed demo data for LUMINA.

This file contains clearly fictional data for development and portfolio purposes.
Run with: python seed.py
"""

from app import create_app, db
from app.models import Service, FAQ, Testimonial, Enquiry

def seed():
    """Populate database with demo data."""
    app = create_app()

    with app.app_context():
        # Clear existing data
        Service.query.delete()
        FAQ.query.delete()
        Testimonial.query.delete()
        Enquiry.query.delete()

        # Services (from config, but also add a few via ORM for demo)
        services = [
            Service(
                name="Portrait Sessions",
                description="Timeless portraits that reveal character and elegance. Perfect for professionals, families, and personal branding.",
                price="$299",
                icon="portrait",
                order=1,
            ),
            Service(
                name="Event Coverage",
                description="Full-day or half-day coverage for weddings, corporate events, and celebrations. Edited gallery delivered within 2 weeks.",
                price="$1,200+",
                icon="event",
                order=2,
            ),
            Service(
                name="Product Photography",
                description="Studio or on-location shots for e-commerce, portfolios, and marketing materials. Includes styling and lighting consultation.",
                price="$499",
                icon="product",
                order=3,
            ),
        ]
        db.session.add_all(services)

        # FAQ
        faq_items = [
            FAQ(
                question="What is your turnaround time for edited photos?",
                answer="For portrait sessions, edited photos are delivered within 5 business days. Event galleries take 10–14 days. Rush delivery available upon request.",
                order=1,
            ),
            FAQ(
                question="Do you offer retouching and editing?",
                answer="Yes, all sessions include professional retouching. Color grading, skin tone adjustment, and background enhancement are standard.",
                order=2,
            ),
            FAQ(
                question="Can I purchase prints or albums?",
                answer="Absolutely. We offer high-quality prints, canvases, and luxury albums. Pricing available upon request.",
                order=3,
            ),
            FAQ(
                question="What's your cancellation policy?",
                answer="Cancellations made 7+ days in advance receive a full refund. Within 7 days, a 50% refund is issued. No-shows forfeit the full fee.",
                order=4,
            ),
            FAQ(
                question="Do you offer package deals?",
                answer="Yes, we offer discounts for multiple sessions and volume orders. Contact us for custom pricing.",
                order=5,
            ),
        ]
        db.session.add_all(faq_items)

        # Testimonials (only approved ones will display)
        testimonials = [
            Testimonial(
                name="Sarah Chen",
                role="Bride",
                message="LUMINA captured every precious moment of our wedding day. The photos are absolutely stunning and timeless.",
                approved=True,
                order=1,
            ),
            Testimonial(
                name="Marcus Johnson",
                role="Founder, TechStart Co.",
                message="Professional, creative, and easy to work with. The product shots took our marketing to the next level.",
                approved=True,
                order=2,
            ),
            Testimonial(
                name="Elena Rodriguez",
                role="Artist",
                message="A portrait session with LUMINA was transformative. They saw me in a way I didn't see myself. Highly recommended.",
                approved=True,
                order=3,
            ),
            Testimonial(
                name="James Park",
                role="Corporate Client",
                message="Pending approval from admin.",
                approved=False,
                order=4,
            ),
        ]
        db.session.add_all(testimonials)

        # Sample enquiries (for demo)
        enquiries = [
            Enquiry(
                name="Demo Enquiry 1",
                email="demo1@example.com",
                phone="+1 (555) 111-1111",
                service="Portrait Sessions",
                preferred_date="2026-10-25",
                message="This is a demo enquiry for portfolio purposes. Please ignore.",
                status="new",
            ),
            Enquiry(
                name="Demo Enquiry 2",
                email="demo2@example.com",
                phone="+1 (555) 222-2222",
                service="Event Coverage",
                preferred_date="2026-11-10",
                message="Another fictional demo enquiry showing the enquiry management system.",
                status="contacted",
            ),
        ]
        db.session.add_all(enquiries)

        db.session.commit()
        print("✓ Database seeded with demo data")
        print("  - 3 Services")
        print("  - 5 FAQs")
        print("  - 4 Testimonials (3 approved)")
        print("  - 2 Sample enquiries")

if __name__ == "__main__":
    seed()
