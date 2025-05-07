import streamlit as st
import pandas as pd
import pymysql
from datetime import date

connection=pymysql.connect(host = "localhost",user = "theertha",password = "Sreekutty@17",database = "nasadata")
cursor=connection.cursor()

st.markdown("""
<h1 style="color: red; margin-top: -60px;">🚀 NASA Asteriod Tracker 🌠</h1>
            """,
unsafe_allow_html=True)

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Filter Range"

def set_tab(tab_name):
    st.session_state.active_tab = tab_name
    
with st.sidebar:
    st.markdown("## ASTEROID APPROACHES☄️")
    
    for tab in ["Filter Range", "Queries"]:
        if st.button(tab, key=f"btn_{tab}", use_container_width=True):
            set_tab(tab)


if st.session_state.active_tab == "Filter Range":
    st.subheader("🔍 Filter Range")

    data =  """
    SELECT
    a.id,
    a.name,
    a.absolute_magnitude_h,
    a.estimated_diameter_min_km,
    a.estimated_diameter_max_km,
    a.is_potentially_hazardous_asteroid,
    ca.astronomica,
    ca.close_approach_date,
    ca.relative_velocity_kmph,
    ca.miss_distance_km,
    ca.orbiting_body
FROM
    asteroids a join close_approach ca on a.id = ca.neo_reference_id
WHERE
    
    a.absolute_magnitude_h >= %s AND a.absolute_magnitude_h <= %s
    AND a.estimated_diameter_min_km >= %s AND a.estimated_diameter_min_km <= %s
    AND a.estimated_diameter_max_km >= %s AND a.estimated_diameter_max_km <= %s
    AND ca.relative_velocity_kmph >= %s AND ca.relative_velocity_kmph <= %s
    AND ca.close_approach_date >= %s AND ca.close_approach_date <= %s
    AND ca.astronomica >= %s AND ca.astronomica <= %s
    AND a.is_potentially_hazardous_asteroid = %s;
    """
   
      # Filters
    col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.3, 1, 0.3, 1])

    with col1:
        absolute_magnitude_h = st.slider("Min Magnitude", 18.16, 30.9, (18.16, 30.9))
    with col2:
        relative_velocity_kmph = st.slider("Relative_velocity_kmph Range", 1909.58, 136268.0, (1909.58, 136268.0))
    with col3:
        close_approach_start_date = st.date_input("Start date", value=date(2024, 1, 1))
    

    col4, spacer3, col5, spacer4, col6 = st.columns([1, 0.3, 1, 0.3, 1])

    with col4:
        min_estimated_diameter = st.slider("Min Estimated Diameter (km)", 0.00, 0.62, (0.00, 0.62))
    with col5:
        astronomica = st.slider("Astronomical Unit", 0.00162219, 0.49321, (0.00162219, 0.49321))
    with col6:
        close_approach_end_date = st.date_input("End date", value=date(2025, 1, 13))
    
    col7, spacer5, col8, spacer6 = st.columns([1, 0.3, 1, 0.3])

    with col7:
        max_estimated_diameter = st.slider("Max Estimated Diameter (km)", 0.00, 1.4, (0.00, 1.4))
    with col8:
       is_potentially_hazardous_asteroid = st.selectbox("Active", ["0", "1"])
        
    values = [
        absolute_magnitude_h[0],
        absolute_magnitude_h[1],
        min_estimated_diameter[0],
        min_estimated_diameter[1],
        max_estimated_diameter[0],
        max_estimated_diameter[1],
        relative_velocity_kmph[0],
        relative_velocity_kmph[1],
        close_approach_start_date,
        close_approach_end_date,
        astronomica[0],
        astronomica[1],
        is_potentially_hazardous_asteroid
]

   #  Filter Trigger Button
    if st.button("Apply Filters"):
        cursor.execute(data, values)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["id","name","absolute_magnitude_h","estimated_diameter_min_km",
                                        "estimated_diameter_max_km", "is_potentially_hazardous_asteroid", "astronomica", 
                                        "close_approach_date","relative_velocity_kmph",
                                        "miss_distance_km","orbiting_body"])
        st.dataframe(df)


    # Queries
elif st.session_state.active_tab == "Queries":
    st.subheader("📊 Queries")
    query =st.selectbox("Options",[
        "1.Count how many times each asteroid has approached Earth",
        "2.Average velocity of each asteroid over multiple approaches",
        "3.List top 10 fastest asteroids",
        "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
        "5. Find the month with the most asteroid approaches",
        "6.Get the asteroid with the fastest ever approach speed",
        "7. Sort asteroids by maximum estimated diameter (descending)",
        "8.Asteroids whose closest approach is getting nearer over time",
        "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
        "10. List names of asteroids that approached Earth with velocity > 50,000 km/h",
        "11. Count how many approaches happened per month",
        "12.Find asteroid with the highest brightness (lowest magnitude value)",
        "13. Get number of hazardous vs non-hazardous asteroids",
        "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
        "15. Find asteroids that came within 0.05 AU(astronomical distance)",
        "16.Find close approaches with a miss distance greater than 100,000 km",
        "17.List the names of potentially hazardous asteroids and their closest miss distance in kilometers",
        "18.List the names and maximum estimated diameters of all asteroids, ordered by their maximum estimated diameter in descending order",
        "19. Find the names of asteroids that have had more than two close approaches",
        "20. Find the average relative velocity of all close approaches"
    ])

    if query == "1.Count how many times each asteroid has approached Earth":
        cursor.execute("""
        select a.name,ca.neo_reference_id,
        count(ca.neo_reference_id) as approach_count
        from asteroids a
        join close_approach ca on a.id = ca.neo_reference_id
        group by a.name,ca.neo_reference_id
        order by approach_count desc;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["neo_reference_id","name", "approach_count"])
        st.dataframe(df)
    
    elif query == "2.Average velocity of each asteroid over multiple approaches":
        cursor.execute("""
        select a.name,ca.neo_reference_id, avg(ca.relative_velocity_kmph) as average_velocity_kmph
        from asteroids a
        join close_approach ca on a.id = ca.neo_reference_id
        group by a.name,ca.neo_reference_id;
        """)
        results=cursor.fetchall()
        df = pd.DataFrame(results, columns=["neo_reference_id","name","average_velocity"])
        st.dataframe(df)
    elif query == "3.List top 10 fastest asteroids":
        cursor.execute(""" 
        select a.name,ca.neo_reference_id, ca.relative_velocity_kmph
        from asteroids a
        join close_approach ca on a.id = ca.neo_reference_id
        order by relative_velocity_kmph desc
        limit 10;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["neo_reference_id","name", "relative_velocity_kmph"])
        st.dataframe(df)
    elif query == "4.Find potentially hazardous asteroids that have approached Earth more than 3 times":
        cursor.execute("""
        select a.name from asteroids a
        join close_approach ca on a.id = ca.neo_reference_id
        where a.is_potentially_hazardous_asteroid = TRUE 
        group by a.id, a.name
        having count(ca.close_approach_date) > 3;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name"])
        st.dataframe(df)
    elif query == "5. Find the month with the most asteroid approaches":
        cursor.execute( """
        select monthname(close_approach_date) as month,
        count(*) as number_of_approaches
        from close_approach
        group by monthname(close_approach_date)
        order by number_of_approaches desc
        limit 1;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["month","number_of_approaches"])
        st.dataframe(df)
    elif query == "6.Get the asteroid with the fastest ever approach speed":
        cursor.execute( """
    select neo_reference_id, 
        relative_velocity_kmph
        from close_approach
        order by relative_velocity_kmph asc
        limit 1;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["neo_reference_id","relative_velocity_kmph"])
        st.dataframe(df)
    elif query == "7. Sort asteroids by maximum estimated diameter (descending)":
        cursor.execute( """
        select id, name, estimated_diameter_max_km
        from asteroids
        order by estimated_diameter_max_km desc;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["id","name","estimated_diameter_max_km"])
        st.dataframe(df)
    elif query == "8.Asteroids whose closest approach is getting nearer over time":
        cursor.execute( """
        select
            a.name,
            ca.close_approach_date,
            ca.miss_distance_km
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        order by ca.miss_distance_km desc, close_approach_date desc;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","close_approach_date","miss_distance_km"])
        st.dataframe(df)
    elif query == "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
        cursor.execute( """
        select
            a.name,
            ca.close_approach_date,
            ca.miss_distance_km
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        order by ca.miss_distance_km asc;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","close_approach_date","miss_distance_km"])
        st.dataframe(df)
    elif query == "10. List names of asteroids that approached Earth with velocity > 50,000 km/h":
        cursor.execute( """
        select a.name
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        where ca.relative_velocity_kmph > 50000;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name"])
        st.dataframe(df)
    elif query == "11. Count how many approaches happened per month":
        cursor.execute( """
        select
            monthname(close_approach_date) as month,
            COUNT(*) as num_approaches
        from close_approach
        group by month
        order by month;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["month","number_of_approaches"])
        st.dataframe(df)
    elif query == "12.Find asteroid with the highest brightness (lowest magnitude value)":
        cursor.execute( """
        select name 
        from asteroids
        order by absolute_magnitude_h asc
        limit 1;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name"])
        st.dataframe(df)
    elif query == "13. Get number of hazardous vs non-hazardous asteroids":
        cursor.execute( """
    select is_potentially_hazardous_asteroid, count(*) as count
        from asteroids
        group by is_potentially_hazardous_asteroid;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["is_potentially_hazardous_asteroid","count"])
        st.dataframe(df)
    elif query == "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance":
        cursor.execute( """
        select a.name, ca.close_approach_date, ca.miss_distance_lunar
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        where ca.miss_distance_lunar < 1;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","close_approach_date","miss_distance_lunar"])
        st.dataframe(df)
    elif query == "15. Find asteroids that came within 0.05 AU(astronomical distance)":
        cursor.execute( """
    select
            a.name,
            ca.close_approach_date,
            ca.astronomica as astronomical
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        where ca.astronomica < 0.05;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","close_approach_date","astronomical"])
        st.dataframe(df)
    elif query == "16.Find close approaches with a miss distance greater than 100,000 km":
        cursor.execute( """
    select  a.name,ca.neo_reference_id,ca.miss_distance_km 
        from close_approach ca
        join asteroids a on ca.neo_reference_id = a.id
        where miss_distance_km > 100000;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","neo_reference_id","miss_distance_km"])
        st.dataframe(df)
    elif query == "17.List the names of potentially hazardous asteroids and their closest miss distance in kilometers":
        cursor.execute( """
    select a.name, min(ca.miss_distance_km) as closest_miss_distance_km
        from asteroids a
        join close_approach ca ON a.id = ca.neo_reference_id
        where a.is_potentially_hazardous_asteroid = TRUE
        group by a.id, a.name;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","closest_miss_distance_km"])
        st.dataframe(df)
    elif query == "18.List the names and maximum estimated diameters of all asteroids, ordered by their maximum estimated diameter in descending order":
        cursor.execute( """
    select name, estimated_diameter_max_km
        from asteroids
        order by estimated_diameter_max_km desc;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name","estimated_diameter_max_km"])
        st.dataframe(df)
    elif query == "19. Find the names of asteroids that have had more than two close approaches":
        cursor.execute( """
    select a.name from asteroids a
        join close_approach ca on a.id = ca.neo_reference_id
        group by a.id, a.name
        having count(ca.close_approach_date) > 2;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["name"])
        st.dataframe(df)
    elif query == "20. Find the average relative velocity of all close approaches":
        cursor.execute( """
        select avg(relative_velocity_kmph) as average_velocity
        from close_approach;
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["average_velocity"])
        st.dataframe(df)