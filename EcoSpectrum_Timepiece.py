import pygame
import sys
import requests
from datetime import datetime, timedelta
import pytz

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 240, 320
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graphical Clock")

# Load background image and rotate it by 90 degrees
background_image = pygame.image.load('rainbow.jpg')
background_image = pygame.transform.scale(background_image, (height, width))  # Note the dimensions swapped
background_image = pygame.transform.rotate(background_image, 90)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font settings
time_font_size = 60
date_font_size = 24
time_font = pygame.font.SysFont('Arial', time_font_size, bold=True)
date_font = pygame.font.SysFont('Arial', date_font_size, bold=True)

# Time settings
local_tz = pytz.timezone('Asia/Kolkata')
last_update = datetime.now(local_tz)
update_interval = timedelta(hours=1)

# Define manual coordinates for time and date
time_x = width - 200 // 2   # X coordinate for time
time_y = height - 650 // 4  # Y coordinate for time
date_x = width - 100 // 2   # X coordinate for date
date_y = time_y + time_font_size + 10  # Y coordinate for date, below the time

def fetch_internet_time():
    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Kolkata")
        data = response.json()
        internet_time = datetime.fromisoformat(data["datetime"]).astimezone(local_tz)
        return internet_time
    except Exception as e:
        print(f"Error fetching time: {e}")
        return None

def draw_text_with_border_and_shadow(text, font, x, y):
    # Render text with anti-aliasing
    text_surface = font.render(text, True, white)
    
    # Create a shadow effect by rendering the text in black with an offset
    shadow_surface = font.render(text, True, black)
    shadow_offset = 2
    
    # Draw shadow
    screen.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
    
    # Draw black border by rendering text in black at different offsets
    border_thickness = 2
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:
                border_surface = font.render(text, True, black)
                screen.blit(border_surface, (x + dx, y + dy))
    
    # Draw the main white text
    screen.blit(text_surface, (x, y))

def main():
    global last_update
    current_time = datetime.now(local_tz)

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update time from internet if an hour has passed
        now = datetime.now(local_tz)
        if now - last_update >= update_interval:
            internet_time = fetch_internet_time()
            if internet_time:
                current_time = internet_time
            last_update = now
        
        # Fill the background with the rotated image
        screen.blit(background_image, (0, 0))
        
        # Update current time
        current_time += timedelta(seconds=1)
        display_time = current_time.strftime("%H:%M:%S")
        display_date = current_time.strftime("%d %b %Y")
        
        # Get the size of the text surfaces
        time_surface = time_font.render(display_time, True, white)
        date_surface = date_font.render(display_date, True, white)
        
        # Set positions for the time and date
        time_rect = time_surface.get_rect(center=(time_x, time_y))
        date_rect = date_surface.get_rect(center=(date_x, date_y))
        
        # Print coordinates
#         print(f"Time coordinates: {time_rect.topleft}")
#         print(f"Date coordinates: {date_rect.topleft}")
        
        # Rotate the text surfaces by 90 degrees
        rotated_time_surface = pygame.transform.rotate(time_surface, 90)
        rotated_date_surface = pygame.transform.rotate(date_surface, 90)
        rotated_time_rect = rotated_time_surface.get_rect(center=(time_x, time_y))
        rotated_date_rect = rotated_date_surface.get_rect(center=(date_x, date_y))
        
        # Create shadow and border effect for the rotated time with anti-aliasing
        shadow_time_surface = pygame.transform.rotate(time_font.render(display_time, True, black), 90)
        shadow_offset = 2
        screen.blit(shadow_time_surface, (rotated_time_rect.x + shadow_offset, rotated_time_rect.y + shadow_offset))
        border_thickness = 2
        for dx in range(-border_thickness, border_thickness + 1):
            for dy in range(-border_thickness, border_thickness + 1):
                if dx != 0 or dy != 0:
                    border_time_surface = pygame.transform.rotate(time_font.render(display_time, True, black), 90)
                    screen.blit(border_time_surface, (rotated_time_rect.x + dx, rotated_time_rect.y + dy))
        
        # Create shadow and border effect for the rotated date with anti-aliasing
        shadow_date_surface = pygame.transform.rotate(date_font.render(display_date, True, black), 90)
        screen.blit(shadow_date_surface, (rotated_date_rect.x + shadow_offset, rotated_date_rect.y + shadow_offset))
        for dx in range(-border_thickness, border_thickness + 1):
            for dy in range(-border_thickness, border_thickness + 1):
                if dx != 0 or dy != 0:
                    border_date_surface = pygame.transform.rotate(date_font.render(display_date, True, black), 90)
                    screen.blit(border_date_surface, (rotated_date_rect.x + dx, rotated_date_rect.y + dy))
        
        # Draw the rotated main white text with anti-aliasing
        screen.blit(rotated_time_surface, rotated_time_rect.topleft)
        screen.blit(rotated_date_surface, rotated_date_rect.topleft)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(1)

if __name__ == "__main__":
    main()
