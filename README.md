# TODOs

## Open Academy
### Access rights
- [x] - Add rule for archs to modify courses
- [x] - Fix compute method for can_modify
- [x] - Add domain based on course level (1..3) - easy (4..7) - medium (8..10) - hard

### Play with ORM
- [x] - Add **account, product** dependencies
- [x] - Add fields to session model
- [x] - Fix **Account Receivable - Account Payable** error
- [x] - Add button **"Invoice teacher"** to session form view
- [x] - Create handler for button

### Reports
- [x] - Create action for report
- [x] - Create report template
- [x] - Insert barcode

### Controllers
- [x] - Create controller with routes
- [x] - Create template for corses
- [x] - Create template for sessions

## Library
### Actions/Views
- [x] - Create menu
- [x] - Tree/form views for Books
- [x] - Tree/form views for Partners
- [x] - Tree/form views for Rentals
- [x] - Tree/form views for Publishers
- [x] - Domain for authors in Books form
- [x] - Search filter by author_ids and isbn

### Model inheritance
- [x] - Add library.copy model
- [x] - Create views for this model

### View inheritance
- [x] - Inherit book view for copy

### Business flow
- [x] - Inherit product.product and res.partner
- [x] - Create library.price model
- [x] - Link library.payment to res.partner
- [x] - Notify clients about payments (email)

### Wizard
- [x] - Create smart button for library.copy (readers_count)
- [x] - Create action for library.copy (Add books)

### Report
- [x] - Create report for res.partner

### Website
- [x] - Add books page with book list
- [x] - Create form for renting book
- [x] - Create fallback form for rented books
- [x] - Set access rule for logged users only

### Misc
- [x] - Add menus to website
- [ ] - Add access groups to library model
- [x] - Fix copy form view