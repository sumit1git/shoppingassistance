"""
Travel planning tools for the chatbot.
Contains hotel recommendations and itinerary suggestions.
"""

# Sample hotel database
HOTELS_DATABASE = {
    "Paris": [
        {
            "name": "Le Meurice",
            "rating": 4.8,
            "price_per_night": "$500-800",
            "description": "Luxury 5-star hotel near Tuileries Garden with fine dining"
        },
        {
            "name": "Hotel Plaza Athénée",
            "rating": 4.7,
            "price_per_night": "$400-700",
            "description": "Historic luxury hotel on Champs-Élysées"
        },
        {
            "name": "Boutique Hotel Marais",
            "rating": 4.5,
            "price_per_night": "$150-300",
            "description": "Charming 4-star hotel in the heart of Le Marais"
        }
    ],
    "Tokyo": [
        {
            "name": "The Peninsula Tokyo",
            "rating": 4.8,
            "price_per_night": "$600-900",
            "description": "Ultra-luxury hotel with stunning views of Tokyo Bay"
        },
        {
            "name": "Mandarin Oriental Tokyo",
            "rating": 4.7,
            "price_per_night": "$500-800",
            "description": "Premium hotel in Nihonbashi with Michelin-starred restaurants"
        },
        {
            "name": "Hotel Gracery Shinjuku",
            "rating": 4.4,
            "price_per_night": "$120-250",
            "description": "Modern 4-star hotel in vibrant Shinjuku district"
        }
    ],
    "New York": [
        {
            "name": "The Plaza Hotel",
            "rating": 4.7,
            "price_per_night": "$600-1000",
            "description": "Iconic luxury hotel overlooking Central Park"
        },
        {
            "name": "The Four Seasons",
            "rating": 4.8,
            "price_per_night": "$700-1200",
            "description": "Ultra-luxury hotel in Midtown Manhattan"
        },
        {
            "name": "Pod Hotel New York",
            "rating": 4.2,
            "price_per_night": "$80-180",
            "description": "Budget-friendly trendy hotel in Hell's Kitchen"
        }
    ],
    "Barcelona": [
        {
            "name": "Hotel Arts Barcelona",
            "rating": 4.7,
            "price_per_night": "$400-700",
            "description": "Luxury beachfront hotel with world-class dining"
        },
        {
            "name": "Ohla Barcelona",
            "rating": 4.6,
            "price_per_night": "$300-600",
            "description": "Modern luxury hotel in Gothic Quarter"
        },
        {
            "name": "Mercer Hotel Barcelona",
            "rating": 4.5,
            "price_per_night": "$200-400",
            "description": "Boutique hotel in Medieval Barcelona with rooftop bar"
        }
    ],
    "Dubai": [
        {
            "name": "Burj Al Arab",
            "rating": 4.9,
            "price_per_night": "$1000-3000",
            "description": "Iconic ultra-luxury 7-star hotel on private island"
        },
        {
            "name": "Atlantis The Palm",
            "rating": 4.6,
            "price_per_night": "$400-900",
            "description": "Luxury resort with aquarium and water park"
        },
        {
            "name": "JA Ocean View Hotel",
            "rating": 4.3,
            "price_per_night": "$150-350",
            "description": "Modern beachfront hotel with great value"
        }
    ]
}

# Sample itinerary templates
ITINERARIES_DATABASE = {
    "Paris": {
        "3_days": [
            "Day 1: Arrive in Paris, settle in hotel, visit Eiffel Tower at sunset, dinner at local bistro",
            "Day 2: Louvre Museum (2-3 hours), Notre-Dame Cathedral, Latin Quarter exploration",
            "Day 3: Champs-Élysées and Arc de Triomphe, Montmartre district, Sacré-Cœur Basilica"
        ],
        "5_days": [
            "Day 1: Eiffel Tower and Trocadéro, Seine River cruise, Champs-Élysées",
            "Day 2: Louvre Museum full day, explore surrounding Marais district",
            "Day 3: Day trip to Versailles Palace and Gardens",
            "Day 4: Montmartre, Sacré-Cœur, Latin Quarter, Panthéon",
            "Day 5: Musée d'Orsay, Seine walk, local shopping, final dinner"
        ],
        "7_days": [
            "Day 1-2: Iconic Paris (Eiffel Tower, Louvre, Notre-Dame)",
            "Day 3: Versailles full day with gardens exploration",
            "Day 4: Montmartre and Northern Paris",
            "Day 5: Day trip to Monet's Gardens at Giverny",
            "Day 6: Latin Quarter, catacombs, local museums",
            "Day 7: Shopping, cafés, relaxation, sunset view"
        ]
    },
    "Tokyo": {
        "3_days": [
            "Day 1: Shibuya Crossing, Harajuku, Meiji Shrine, dinner in Shinjuku",
            "Day 2: Senso-ji Temple, Tsukiji Outer Market, Akihabara tech district",
            "Day 3: Team Lab digital art museum, Roppongi Hills, Minato ward exploration"
        ],
        "5_days": [
            "Day 1: Shinjuku and Shibuya districts, nightlife in Kabukicho",
            "Day 2: Asakusa Temple, traditional shopping streets, boat ride on Sumida River",
            "Day 3: Day trip to Mount Fuji (Hakone or Kawaguchiko)",
            "Day 4: Akihabara, Ginza luxury shopping, teamLab museum",
            "Day 5: Imperial Palace, Meiji Shrine, local parks and cafés"
        ],
        "7_days": [
            "Day 1-2: Tokyo exploration (Shinjuku, Shibuya, Harajuku)",
            "Day 3: Traditional Tokyo (Asakusa, Senso-ji)",
            "Day 4: Day trip to Mount Fuji and Five Lakes",
            "Day 5: Akihabara, Ginza, and modern Tokyo",
            "Day 6: Side trip to Nikko or Kamakura",
            "Day 7: Relaxation, shopping, local experiences"
        ]
    },
    "New York": {
        "3_days": [
            "Day 1: Times Square, Broadway show, Central Park walk",
            "Day 2: Statue of Liberty and Ellis Island day trip, Brooklyn Bridge walk",
            "Day 3: Museum of Natural History or Metropolitan Museum of Art, Times Square"
        ],
        "5_days": [
            "Day 1: Manhattan highlights (Empire State Building, Times Square, Theater District)",
            "Day 2: Central Park full day, museums nearby",
            "Day 3: Downtown Manhattan (Wall Street, 9/11 Memorial, Brooklyn Bridge)",
            "Day 4: Day trip to Statue of Liberty and Ellis Island",
            "Day 5: Brooklyn exploration (Williamsburg, DUMBO, Coney Island)"
        ],
        "7_days": [
            "Day 1-2: Midtown Manhattan major attractions",
            "Day 3: Lower Manhattan and Financial District",
            "Day 4: Day trip to Statue of Liberty and Ellis Island",
            "Day 5: Brooklyn and Queens exploration",
            "Day 6: Museums and cultural institutions",
            "Day 7: Shopping, local neighborhoods, dining experiences"
        ]
    },
    "Barcelona": {
        "3_days": [
            "Day 1: Sagrada Familia, Gothic Quarter, Las Ramblas",
            "Day 2: Park Güell, Gaudí's Casa Batlló and Casa Milà",
            "Day 3: Barcelona Beach, Olympic Village, Montjuïc Castle"
        ],
        "5_days": [
            "Day 1: Sagrada Familia, Gothic Quarter exploration",
            "Day 2: Park Güell, Gaudí's architectural wonders",
            "Day 3: Barcelona beaches and Olympic sites",
            "Day 4: Montjuïc Castle, museums, cable car experience",
            "Day 5: Local neighborhoods, Boqueria Market, nightlife"
        ],
        "7_days": [
            "Day 1-2: Sagrada Familia and Gothic Quarter",
            "Day 3: Park Güell and Gaudí's masterpieces",
            "Day 4: Beaches and seaside activities",
            "Day 5: Montjuïc exploration with museums and castle",
            "Day 6: Day trip to Montserrat Monastery",
            "Day 7: Shopping, local cuisine, relaxation"
        ]
    },
    "Dubai": {
        "3_days": [
            "Day 1: Burj Khalifa, Downtown Dubai, Dubai Fountain shows",
            "Day 2: Desert Safari with traditional Bedouin dinner",
            "Day 3: Beach clubs, Palm Jumeirah, Atlantis The Palm"
        ],
        "5_days": [
            "Day 1: Burj Khalifa and Downtown Dubai exploration",
            "Day 2: Desert Safari and traditional experiences",
            "Day 3: Beach day at Palm Jumeirah or Public Beach",
            "Day 4: Gold Souk, Spice Souk, traditional old Dubai",
            "Day 5: Shopping malls, water sports, relaxation"
        ],
        "7_days": [
            "Day 1-2: Modern Dubai (Burj Khalifa, Downtown, Malls)",
            "Day 3: Desert Safari and Bedouin culture",
            "Day 4: Beach and water activities",
            "Day 5: Traditional Dubai (souks, old town, heritage)",
            "Day 6: Day trip to Abu Dhabi or activities",
            "Day 7: Shopping, spa, final experiences"
        ]
    }
}


def get_hotel_recommendations(destination: str) -> str:
    """
    Get top hotel recommendations for a given destination.
    
    Args:
        destination: The travel destination (city name)
    
    Returns:
        Formatted string with hotel recommendations
    """
    destination_title = destination.title()
    
    if destination_title not in HOTELS_DATABASE:
        return f"Sorry, I don't have hotel recommendations for {destination} yet. Available destinations: {', '.join(HOTELS_DATABASE.keys())}"
    
    hotels = HOTELS_DATABASE[destination_title]
    response = f"\n🏨 **Top Hotels in {destination_title}:**\n\n"
    
    for i, hotel in enumerate(hotels, 1):
        response += f"{i}. **{hotel['name']}**\n"
        response += f"   ⭐ Rating: {hotel['rating']}/5\n"
        response += f"   💰 Price: {hotel['price_per_night']} per night\n"
        response += f"   📝 {hotel['description']}\n\n"
    
    return response


def get_itinerary_suggestion(destination: str, duration: str) -> str:
    """
    Get a suggested itinerary for a destination based on duration.
    
    Args:
        destination: The travel destination
        duration: Duration like "3 days", "5 days", "7 days"
    
    Returns:
        Formatted string with itinerary
    """
    destination_title = destination.title()
    
    if destination_title not in ITINERARIES_DATABASE:
        return f"Sorry, I don't have itinerary suggestions for {destination} yet. Available destinations: {', '.join(ITINERARIES_DATABASE.keys())}"
    
    # Parse duration to match database format
    duration_lower = duration.lower().strip()
    duration_key = None
    
    if "3" in duration_lower:
        duration_key = "3_days"
    elif "5" in duration_lower:
        duration_key = "5_days"
    elif "7" in duration_lower:
        duration_key = "7_days"
    else:
        available = list(ITINERARIES_DATABASE[destination_title].keys())
        available_formatted = ", ".join([k.replace('_', ' ').title() for k in available])
        return f"I have itineraries for: {available_formatted}. Please specify 3, 5, or 7 days."
    
    if duration_key not in ITINERARIES_DATABASE[destination_title]:
        available = list(ITINERARIES_DATABASE[destination_title].keys())
        available_formatted = ", ".join([k.replace('_', ' ').title() for k in available])
        return f"I have itineraries for: {available_formatted}."
    
    itinerary = ITINERARIES_DATABASE[destination_title][duration_key]
    duration_display = duration_key.replace('_', ' ').title()
    
    response = f"\n📅 **{duration_display} Itinerary for {destination_title}:**\n\n"
    
    for day_plan in itinerary:
        response += f"✈️ {day_plan}\n"
    
    response += f"\n**Travel Tips:**\n"
    response += f"- Book accommodations in advance\n"
    response += f"- Purchase travel insurance\n"
    response += f"- Check visa requirements\n"
    response += f"- Learn basic local phrases\n"
    
    return response
