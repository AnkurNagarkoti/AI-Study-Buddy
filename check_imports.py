try:
    import dotenv
    print("✅ dotenv found")
except ImportError as e:
    print(f"❌ dotenv NOT found: {e}")

try:
    import matplotlib
    print("✅ matplotlib found")
except ImportError as e:
    print(f"❌ matplotlib NOT found: {e}")
