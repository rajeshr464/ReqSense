# Mobile Responsiveness Optimization

Improve the UI/UX for mobile users by implementing responsive navigation, collapsible sidebars, and fluid layouts across the dashboard and landing pages.

## Proposed Changes

### Dashboard

#### [MODIFY] [base_dashboard.html](file:///f:/ReqSense/templates/dashboard/base_dashboard.html)
- Add a mobile-only top bar with a hamburger menu button.
- Make the sidebar collapsible on mobile using a simple JavaScript toggle.
- Convert the fixed sidebar to `transform -translate-x-full md:translate-x-0` to hide it on small screens.
- Add an overlay that appears when the mobile menu is open.
- Adjust the main content margin from fixed `ml-64` to responsive `md:ml-64`.

#### [MODIFY] [index.html](file:///f:/ReqSense/templates/dashboard/index.html)
- Ensure all tables and grid containers behave correctly on small screens.

### Landing Page

#### [MODIFY] [landing.html](file:///f:/ReqSense/templates/dashboard/landing.html)
- Implement a mobile menu toggle for the header navigation.
- Adjust hero section font sizes and paddings for better readability on phones.

### Authentication

#### [MODIFY] [login.html](file:///f:/ReqSense/templates/accounts/login.html) & [register.html](file:///f:/ReqSense/templates/accounts/register.html)
- Ensure branding and form sections stack vertically on mobile.
- Adjust vertical spacing and font sizes.

## Verification Plan

### Manual Verification
1. Open the application on a mobile device or use browser developer tools (Mobile simulation).
2. Verify the hamburger menu opens and closes the sidebar.
3. Check the landing page for overlapping elements on small screens.
4. Ensure the dashboard table is scrollable and readable.
5. Verify the login and registration forms are easy to use on a phone.
