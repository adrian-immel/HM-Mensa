import sys
from datetime import datetime
import pytz
import location


def render_barometer_html(loc: location):
    current_capacity = loc.capacity_level_in_percent
    timestamp = loc.timestamp
    location_name = loc.name
    output_file = loc.html_file_name
    total_height = 300  # Height of the thermometer column in px
    fill_height = int((current_capacity / 100) * total_height)+38
    if fill_height > 295:
        fill_height = 295
    
    # Format the timestamp
    update_time = datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Berlin')).strftime('%H:%M')

    if current_capacity < 33:
        fill_color = "#00e64d"  # Green
    elif current_capacity < 67:
        fill_color = "#ffa500"  # Orange
    else:
        fill_color = "#ff3333"  # Red

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{location_name} Capacity</title>
    <style>
        body {{
            font-family: sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 0;
        }}

        .page-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}

        /* Title Styles */
        .location-title {{
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #333;
        }}

        /* Hamburger Menu Styles */
        .hamburger-menu {{
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 100;
            cursor: pointer;
        }}

        .hamburger-icon {{
            width: 30px;
            height: 20px;
            position: relative;
            cursor: pointer;
        }}

        .hamburger-icon span {{
            display: block;
            position: absolute;
            height: 3px;
            width: 100%;
            background: #333;
            border-radius: 3px;
            transition: 0.25s ease-in-out;
        }}

        .hamburger-icon span:nth-child(1) {{ top: 0px; }}
        .hamburger-icon span:nth-child(2) {{ top: 8px; }}
        .hamburger-icon span:nth-child(3) {{ top: 16px; }}

        .nav-menu {{
            position: fixed;
            left: -250px;
            top: 0;
            width: 250px;
            height: 100%;
            background-color: white;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            transition: 0.3s;
            z-index: 99;
        }}

        .nav-menu.active {{
            left: 0;
        }}

        .nav-menu ul {{
            list-style: none;
            padding: 60px 0 0 0;
            margin: 0;
        }}

        .nav-menu ul li {{
            padding: 15px 25px;
        }}

        .nav-menu ul li a {{
            color: #333;
            text-decoration: none;
            font-size: 16px;
        }}

        .nav-menu ul li a:hover {{
            color: #666;
        }}

        .content-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .container {{
            display: flex;
            align-items: flex-end;
            gap: 40px;
        }}

        .thermometer {{
            position: relative;
            width: 40px;
            height: {total_height + 40}px;
            background-color: #e0e0e0;
            border-radius: 20px;
        }}

        .bulb {{
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 60px;
            background-color: {fill_color};
            border: 4px solid #e0e0e0;
            border-radius: 50%;
            z-index: 2;
        }}

        .fill {{
            position: absolute;
            bottom: 30px;
            left: 0;
            width: 100%;
            height: {fill_height}px;
            background-color: {fill_color};
            border-radius: 20px;
            z-index: 1;
        }}

        .labels {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: {total_height}px;
            margin-bottom: 55px;
        }}

        .labels span {{
            font-size: 1rem;
            line-height: 1;
        }}
        
        .update-time {{
            text-align: center;
            color: #666;
            margin-top: 1rem;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <!-- Hamburger Menu -->
    <div class="hamburger-menu" onclick="toggleMenu()">
        <div class="hamburger-icon">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="nav-menu">
        <ul>
            <li><a href="index.html">Mensa Lothstr.</a></li>
            <li><a href="mensa_pasing.html">Mensa Pasing</a></li>
            <li><a href="cafe_karl.html">StuCafe Karlstr.</a></li>
            <li><a href="cafe_loth.html">StuCafe Lothstr.</a></li>
            <li><a href="cafe_pasing.html">StuCafe Pasing</a></li>
        </ul>
    </nav>

    <div class="page-wrapper">
        <div class="content-wrapper">
            <h1 class="location-title">{location_name}</h1>
            <div class="container">
                <div class="thermometer">
                    <div class="fill"></div>
                    <div class="bulb"></div>
                </div>
                <div class="labels">
                    <span>Am Limit</span>
                    <span>Langsam wird's kuschlig</span>
                    <span>Die Schlange wird länger</span>
                    <span>Alles Gut</span>
                </div>
            </div>
            <div class="update-time">
                Letztes Update: {update_time}
            </div>
        </div>
    </div>

    <script>
        function toggleMenu() {{
            document.querySelector('.nav-menu').classList.toggle('active');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.querySelector('.nav-menu');
            const hamburger = document.querySelector('.hamburger-menu');
            if (!menu.contains(event.target) && !hamburger.contains(event.target)) {{
                menu.classList.remove('active');
            }}
        }});
    </script>
</body>
</html>
"""
    filename = (sys.path[0] + r'/../output/' + output_file)
    with open(filename, "w") as f:
        f.write(html)

    print(f"Generated {output_file} with {current_capacity}% capacity.")
