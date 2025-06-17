# 🍵 Teabuddy - Streamlit Version

A multilingual Streamlit web application that recommends personalized chai recipes based on your mood and health, with interactive step-by-step cooking guidance.

## Features

- **Multilingual Support**: English, हिंदी (Hindi), and বাংলা (Bengali)
- **Personalized Recommendations**: Based on mood and health state
- **Interactive Cooking**: Step-by-step guidance with visual progress
- **Responsive Design**: Works on desktop and mobile devices
- **Celebration Effects**: Balloons animation upon completion
- **Recipe Database**: Multiple chai varieties with detailed instructions

## Quick Start

### 1. Install Dependencies

\`\`\`bash
pip install streamlit
\`\`\`

### 2. Run the Application

\`\`\`bash
streamlit run app.py
\`\`\`

The application will open in your browser at `http://localhost:8501`

## Project Structure

\`\`\`
teabuddy-streamlit/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/                       # Data files
    ├── all_chai_recipes.json   # Recipe database
    ├── recommendation_map.json # Mood/health mappings
    └── lang/                   # Translation files
        ├── en.json             # English translations
        ├── hi.json             # Hindi translations
        └── bn.json             # Bengali translations
\`\`\`

## Usage

1. **Language Selection**: Choose your preferred language on first visit
2. **Input Preferences**: Select your current mood and health state
3. **Get Recommendation**: Receive a personalized chai recipe
4. **Interactive Cooking**: Follow step-by-step instructions
5. **Celebrate**: Enjoy the celebration when you're done!

## Features Overview

### Language Support
- Automatic language detection and switching
- Complete UI translation for all supported languages
- Localized recipe names and instructions

### Recipe Recommendations
- Mood-based suggestions (Happy, Sad, Tired, Stressed, Creative)
- Health-based filtering (Normal, Cold/Flu, Upset Stomach, Low Energy)
- Smart fallback system for missing combinations

### Interactive Cooking
- Step-by-step visual guidance
- Heat level indicators (Low, Medium, High)
- Duration display for each step
- Progress tracking with visual feedback
- Completion celebration with balloons

### Responsive Design
- Mobile-friendly interface
- Clean, modern UI with custom CSS
- Accessible color schemes and typography
- Intuitive navigation

## Customization

### Adding New Recipes

Edit `data/all_chai_recipes.json` and add new recipe objects:

\`\`\`json
{
  "recipe_id": {
    "name": {
      "en": "English Name",
      "hi": "हिंदी नाम",
      "bn": "বাংলা নাম"
    },
    "description": {
      "en": "English description",
      "hi": "हिंदी विवरण",
      "bn": "বাংলা বর্ণনা"
    },
    "ingredients": ["ingredient 1", "ingredient 2"],
    "steps": [
      {
        "instruction": {
          "en": "English instruction",
          "hi": "हिंदी निर्देश",
          "bn": "বাংলা নির্দেশ"
        },
        "duration": 300,
        "heat": "medium"
      }
    ],
    "total_time": 900
  }
}
\`\`\`

### Adding New Languages

1. Create a new JSON file in `data/lang/` (e.g., `fr.json`)
2. Add translations for all UI elements
3. Update the language selector in `app.py`

### Customizing Recommendations

Edit `data/recommendation_map.json` to modify mood/health combinations and their corresponding recipe suggestions.

## Streamlit-Specific Features

### Session State Management
- Persistent language selection
- Step progress tracking
- Timer state management

### Interactive Elements
- Real-time progress bars
- Dynamic step status updates
- Celebration effects with `st.balloons()`

### Responsive Layout
- Column-based layouts for different screen sizes
- Adaptive component sizing
- Mobile-optimized controls

## Development

### Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Make changes and see them reflected immediately

### Deployment Options

#### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click

#### Other Platforms
- Heroku: Add `setup.sh` and `Procfile`
- Docker: Create `Dockerfile` with Streamlit configuration
- AWS/GCP: Use container services

## Browser Requirements

- Modern browser with JavaScript enabled
- Streamlit requires WebSocket support
- Responsive design works on mobile devices

## Troubleshooting

### Common Issues

1. **Port already in use**: Use `streamlit run app.py --server.port 8502`
2. **Data files not found**: Ensure `data/` directory exists with JSON files
3. **Language not switching**: Clear browser cache and refresh

### Performance Tips

- Use `@st.cache_data` for data loading functions
- Minimize session state usage for better performance
- Optimize images and assets for faster loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Streamlit team for the amazing framework
- Contributors to the chai recipe database
- Translation contributors for multilingual support
\`\`\`

This Streamlit version provides:
- Clean, modern interface optimized for Streamlit
- Full multilingual support with easy language switching
- Interactive step-by-step cooking with visual progress
- Responsive design that works on all devices
- Celebration effects using Streamlit's built-in balloons
- Easy deployment options (Streamlit Cloud, Heroku, etc.)
- Session state management for persistent user experience
\`\`\`

This Streamlit version of Teabuddy provides all the core functionality of the original Flask app but optimized for Streamlit's reactive framework. Key features include:

**Streamlit-Specific Advantages:**
- **Instant Reactivity**: No need for manual page refreshes
- **Built-in Widgets**: Native select boxes, buttons, and progress bars
- **Session State**: Persistent user data across interactions
- **Easy Deployment**: One-click deployment to Streamlit Cloud
- **Mobile Responsive**: Automatically adapts to different screen sizes

**Interactive Features:**
- Language selection with immediate UI updates
- Mood/health input with real-time validation
- Step-by-step cooking with visual progress tracking
- Celebration effects using Streamlit's balloons
- Timer simulation with progress bars

**Technical Implementation:**
- Clean separation of data, logic, and presentation
- Cached data loading for better performance
- Custom CSS for enhanced styling
- Fallback systems for missing data files
- Comprehensive error handling

To run the application:
1. Install Streamlit: `pip install streamlit`
2. Run: `streamlit run app.py`
3. Open `http://localhost:8501` in your browser

The app maintains all the multilingual capabilities and recipe recommendation logic while providing a more modern, interactive user experience through Streamlit's framework.
