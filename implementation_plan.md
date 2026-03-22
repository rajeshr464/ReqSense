# Global Aesthetic Synchronization Plan

Unify the visual identities of the internal Dashboard Hub, AI Query Terminal, and Analytics Reports with the recently overhauled Landing and Authentication modules.

## User Review Required
> [!IMPORTANT]
> This change will transition the internal application from a Dark/Material 3 theme to a Light/Open Sans theme. This significantly alters the visual density of the dashboard.

## Proposed Changes

### 1. Base Dashboard Architecture
#### [MODIFY] [templates/dashboard/base_dashboard.html](file:///f:/ReqSense/templates/dashboard/base_dashboard.html)
- Remove `class="dark"`.
- Switch font stack to `Open Sans`.
- Redefine Tailwind color tokens to match landing page:
    - Primary: `#7e22ce` (Purple)
    - Secondary: `#ec4899` (Pink)
    - Surface: White/Light Gray
- Update the Logo in the Header and Sidebar to use the Font Awesome `chart-bar` icon.
- Adjust the Sidebar to a clean light design with subtle borders.

### 2. Information Density & Component Overlays
#### [MODIFY] [templates/dashboard/index.html](file:///f:/ReqSense/templates/dashboard/index.html) (Data Management)
- Update "Dropzone" and "Dataset Cards" to use white surfaces and light shadows.
#### [MODIFY] [templates/dashboard/view.html](file:///f:/ReqSense/templates/dashboard/view.html) (Intelligence Overview)
- Overhaul KPI cards and Chart containers to match the bright aesthetic.
#### [MODIFY] [templates/dashboard/chat.html](file:///f:/ReqSense/templates/dashboard/chat.html) (AI Query)
- Synchronize chat bubbles. User bubbles should use the Purple-to-Pink gradient.
- Ensure Chart.js defaults (gridlines/fonts) are updated for light backgrounds.
#### [MODIFY] [templates/dashboard/reports.html](file:///f:/ReqSense/templates/dashboard/reports.html) (Reports Hub)
- Align report card styles and export buttons.

## Verification Plan
### Automated Tests
- Run `runserver` and visually inspect the transition from dark to light.
- Verify that the "Add Dataset" modal and "AI Chat" inputs remain legible and contrast-heavy.
- Confirm branding consistency (Logo/Colors) across at least 3 distinct internal routes.
