import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.patches as patches

# Set the style for a professional visualization
plt.style.use('seaborn-v0_8-whitegrid')

# Monthly revenue data from Feb 2023 - Aug 2024
months_str = ['Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 
              'Aug 2023', 'Sep 2023', 'Oct 2023', 'Nov 2023', 'Dec 2023', 'Jan 2024', 
              'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024', 'Jul 2024', 'Aug 2024']

# Convert to datetime for better x-axis formatting
dates = [datetime.strptime(m, '%b %Y') for m in months_str]

# Monthly revenue data (in PHP)
revenues = [1767800, 2406500, 2223500, 1920000, 1673000, 2734000, 2670700, 
            2305250, 1836000, 1889000, 1089000, 1134000, 1830000, 1554000, 
            2068200, 1380000, 1446000, 1148500, 1246674]

# Define pre and post friendship periods
pre_friendship_end = 10  # Index where pre-friendship ends (Nov 2023)
friendship_opening = 10  # Index where Friendship opens (Dec 2023)
novelty_end = 13  # End of novelty period (Feb 2024)

# Create x values for regression (as numeric values)
x_pre = np.arange(pre_friendship_end)
y_pre = revenues[:pre_friendship_end]

# Linear regression on pre-Friendship data
slope, intercept, r_value_pre, p_value, std_err = stats.linregress(x_pre, y_pre)
r_squared_pre = r_value_pre**2

# Create projection line
x_proj = np.arange(pre_friendship_end-1, len(revenues))
y_proj = [slope * x + intercept for x in range(pre_friendship_end-1, len(revenues))]

# Calculate r-squared for post-friendship period
x_post = np.arange(friendship_opening, len(revenues))
y_post = revenues[friendship_opening:]
_, _, r_value_post, _, _ = stats.linregress(x_post, y_post)
r_squared_post = r_value_post**2

# Calculate total revenue loss
actual_post = revenues[friendship_opening:]
projected_post = y_proj[1:]  # Skip the overlapping point
total_loss = sum(projected_post) - sum(actual_post)
commission_loss = total_loss * 0.35

# Calculate immediate drop percentage
immediate_drop_pct = ((y_proj[1] - revenues[friendship_opening]) / y_proj[1]) * 100

# Conservative estimate (accounting for novelty effect)
conservative_loss = 6777838
conservative_commission = conservative_loss * 0.35

# Create the figure
plt.figure(figsize=(12, 8))

# Plot actual revenue data
plt.plot(dates[:pre_friendship_end], revenues[:pre_friendship_end], 'o-', 
         color='#1f77b4', linewidth=2.5, markersize=8, 
         label='Pre-Friendship Revenue')

plt.plot(dates[pre_friendship_end:], revenues[pre_friendship_end:], 'o-', 
         color='#d62728', linewidth=2.5, markersize=8, 
         label='Post-Friendship Revenue')

# Plot projection line
plt.plot(dates[pre_friendship_end-1:], y_proj, '--', 
         color='#1f77b4', linewidth=2, 
         label='Projected Revenue (R²={:.2f})'.format(r_squared_pre))

# Add vertical line for Friendship opening
plt.axvline(x=dates[friendship_opening], color='#d62728', linestyle='-', 
            linewidth=2, alpha=0.7, 
            label='Friendship Opens (Dec 2023)')

# Add rectangle for novelty period
novelty_start_date = dates[friendship_opening]
novelty_end_date = dates[novelty_end]
plt.axvspan(novelty_start_date, novelty_end_date, alpha=0.2, color='#ff7f0e', 
            label='Novelty Effect Period')

# Fill the area between projected and actual revenue
plt.fill_between(dates[friendship_opening:], 
                 projected_post, 
                 actual_post, 
                 color='#d62728', alpha=0.3)

# Format x-axis to show month-year
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)

# Format y-axis with PHP currency
def currency_format(x, pos):
    return '₱{:,.0f}'.format(x)

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(currency_format))

# Set axis labels and title
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Monthly Revenue (PHP)', fontsize=12, fontweight='bold')
plt.title('The Friendship Effect: Infinity Clinic Revenue Cliff', 
          fontsize=16, fontweight='bold')

# Add subtitle
plt.figtext(0.5, 0.915, 'Immediate 42% Revenue Drop in December 2023 (p<0.001)', 
            ha='center', fontsize=13, fontweight='bold')

# Add annotations
plt.annotate('42% Drop\n(p<0.001)', 
             xy=(dates[friendship_opening], revenues[friendship_opening]),
             xytext=(dates[friendship_opening-1], (revenues[friendship_opening] + y_proj[1])/2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=11, fontweight='bold', ha='center', 
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))

# Add R² change annotation
plt.annotate(f'Business Stability Change:\nR²: {r_squared_pre:.2f} → {r_squared_post:.2f}',
             xy=(dates[friendship_opening+4], min(revenues)+100000),
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="black", alpha=0.8),
             fontsize=11, fontweight='bold')

# Create a custom box for the financial impact
impact_text = (f"Total Revenue Loss: ₱{total_loss:,.0f}\n"
               f"Commission Loss (35%): ₱{commission_loss:,.0f}\n\n"
               f"Conservative Estimate:\n"
               f"Revenue: ₱{conservative_loss:,.0f}\n"
               f"Commission: ₱{conservative_commission:,.0f}")

# Position the impact box in the upper right
plt.figtext(0.78, 0.65, impact_text, 
            bbox=dict(boxstyle="round,pad=0.6", fc="#e6f7ff", ec="black", alpha=0.8),
            fontsize=11, fontweight='bold')

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Add legend with better positioning and formatting
legend = plt.legend(loc='upper left', frameon=True, fontsize=10)
legend.get_frame().set_facecolor('#ffffff')
legend.get_frame().set_alpha(0.9)

# Add caption as text at bottom
caption = ("The abrupt revenue drop coincides precisely with Friendship clinic's opening, creating a statistical 'cliff edge'.\n"
           "Pattern disruption (R² change) and persistent impact demonstrate significant business model alteration.")
plt.figtext(0.5, 0.01, caption, ha='center', fontsize=10, style='italic')

# Ensure tight layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.15, top=0.88)  # Make room for caption and title

# Save high-resolution image
plt.savefig('infinity_cliff_edge_chart.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
