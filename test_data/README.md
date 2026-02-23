# RLM Test Data - Fragmentation Demonstration

## Purpose
These CSV files are designed to demonstrate how **dspy.RLM** handles context fragmentation better than traditional RAG.

## Test Files

### 📄 `feedback_batch_1.csv` (10 items)
**Themes introduced:**
- 🔋 **Battery Issues**: Drain, short life, unreliable indicator
- 📸 **Camera Quality**: Mixed reviews, low-light problems, crashes
- 🎨 **UI Problems**: Confusing menus, cluttered interface

### 📄 `feedback_batch_2.csv` (10 items)
**Themes continued:**
- 🔋 **Battery Issues**: Loose charging port, overheating, health degradation
- 📸 **Camera Quality**: Good zoom, poor low-light, creative filters
- 🎨 **UI Problems**: Navigation issues, gesture controls, font size

### 📄 `feedback_batch_3.csv` (10 items)
**Themes concluded:**
- 🔋 **Battery Issues**: Optimization doesn't work, standby drain, fast charging damage
- 📸 **Camera Quality**: Slow launch, excellent portrait mode, degradation after updates
- 🎨 **UI Problems**: Non-descriptive icons, inconsistent dark mode, broken search
- 📊 **Summary feedback**: Overall assessment mentioning all three themes

## The Fragmentation Problem

### Traditional RAG Approach:
```
Upload Batch 1 → Chunks stored separately
Upload Batch 2 → More chunks stored separately  
Upload Batch 3 → Even more chunks stored separately

Query: "What are the main battery issues?"
Result: Retrieves random battery chunks, misses the pattern
❌ No hierarchical understanding
❌ Can't connect related issues across batches
❌ Loses context about severity and frequency
```

### RLM Approach:
```
Upload Batch 1 → RLM writes code to group by theme
                 → Identifies: Battery (critical), Camera (mixed), UI (poor)

Upload Batch 2 → RLM updates hierarchical understanding
                 → Battery: Now includes charging issues
                 → Camera: Adds zoom quality insights
                 → UI: Expands navigation problems

Upload Batch 3 → RLM completes hierarchical analysis
                 → Battery: Full picture (drain + charging + health)
                 → Camera: Complete assessment (quality + performance)
                 → UI: Comprehensive issues (design + functionality)

Query: "What are the main battery issues?"
Result: Hierarchical summary of ALL battery issues
✅ Groups related feedback across batches
✅ Identifies patterns and severity
✅ Maintains context and relationships
```

## Expected RLM Output

When all three batches are ingested, RLM should produce:

```python
{
  'themes': ['battery', 'camera', 'ui', 'build_quality'],
  'critical_issues': [
    'battery_drain',
    'ui_complexity',
    'charging_problems'
  ],
  'sentiment': 'negative',
  'hierarchical_summary': '''
    Three critical themes emerged:
    
    1. BATTERY (Most Critical):
       - Fast drain during normal use and video calls
       - Unreliable percentage indicator
       - Charging port issues and overheating
       - Health degradation from fast charging
       - Standby drain problems
    
    2. UI/UX (Major Issue):
       - Confusing menu structure
       - Poor navigation and gesture controls
       - Inconsistent dark mode
       - Accessibility issues (font size)
    
    3. CAMERA (Mixed):
       - Excellent: Portrait mode, zoom, filters
       - Poor: Low-light performance, app crashes, slow launch
  '''
}
```

## How to Test

1. **Upload Batch 1**: See initial theme identification
2. **Upload Batch 2**: Watch RLM update hierarchical understanding
3. **Upload Batch 3**: Observe complete hierarchical analysis
4. **Query**: "What are the battery problems?" → Should get comprehensive answer
5. **Compare**: Try same with traditional RAG (would miss connections)

## Key Demonstration Points

✅ **Hierarchical Grouping**: RLM groups related feedback across batches
✅ **Pattern Recognition**: Identifies recurring themes automatically
✅ **Context Preservation**: Maintains relationships between issues
✅ **Adaptive Analysis**: Updates understanding as more data arrives
✅ **Code Transparency**: Can see Python code RLM writes to analyze
