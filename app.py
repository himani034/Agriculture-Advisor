import streamlit as st
import pandas as pd
import joblib


st.set_page_config(page_title="Sustainable Agriculture Advisor", layout="centered")

st.image("agriculture.jpg", width=800)


from fpdf import FPDF
import base64
def generate_pdf(score, insights, inputs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(34, 139, 34)
    pdf.set_font("Arial" , 'B', 16)
    pdf.cell(200, 10, txt="Sustainability Report", ln=True, align='C')
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", size=12)

    pdf.ln(10)
    pdf.cell(200,10,txt=f"Predicted Sustainability Score: {score:.2f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Suggestions:", ln=True)
    for i in insights:
        pdf.multi_cell(0, 10,f"- {i}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="your Inputs:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in inputs.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    return pdf.output(dest='s').encode('latin-1')

st.markdown("""
    <style>
    body {
        background-color: #f6fbf4;
        font-family: 'Segoe UI', sans-serif;    
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["prediction", "Tips"])

model = joblib.load("model.pkl")
le_crop = joblib.load("crop_encoder.pkl")
df = pd.read_csv("farmer_advisor_dataset.csv", sep="\t")

if page == "prediction":
    # st.title("Sustainable Agriculture Advisor")
    st.markdown("""
       <h1 style='text-align: centre; color: #2e7d32; font-size: 36px; font-family: "Segoe UI", sans-serif;'>
                Sustainable Agriculture Advisor
       </h1>
""", unsafe_allow_html=True)
    st.markdown("Get a prediction of your crop sustainability score based on key farming parameters")
    st.markdown("---")



st.header("Soil and Weather Information")
col1, col2 = st.columns(2)
with col1:
    soil_pH = st.number_input("Soil pH", value=6.5)
    temperature = st.number_input("Temperature (°C)", value=25)
    fertilizer_usage = st.number_input("Fertilizer Usage (Kg)", value=50)

with col2:
    soil_moisture = st.number_input("Soil Moisture", value=22)
    rainfall = st.number_input("Rainfall (mm)", value=100)
    pesticide_usage = st.number_input("Pesticide Usage (Kg)", value=10)

st.header("Crop Details")
crop_type = st.selectbox("Crop Type", le_crop.classes_)
crop_yield = st.number_input("Crop Yield (ton)", value=2.5) 


if st.button("Predict Sustainability Score"):
    with st.spinner("Analyzing your inputs."):
        try:

            import time
            placeholder = st.empty()
            placeholder.info("Starting analysis.. ")
            time.sleep(1)
            placeholder.warning("Checking input quality..")
            time.sleep(1)
            placeholder.success("Generating final predictipn!")
            time.sleep(0.5)
            placeholder.empty()

            crop_encoded = le_crop.transform([crop_type])[0]
            input_data = pd.DataFrame([{
               'Soil_pH': soil_pH,
               'Soil_Moisture': soil_moisture,
               'Temperature_C': temperature,
               'Rainfall_mm': rainfall,
               'Crop_Type': crop_encoded,
               'Fertilizer_Usage_kg': fertilizer_usage,
               'Pesticide_Usage_kg': pesticide_usage,
               'Crop_Yield_ton': crop_yield
            }])
            result = model.predict(input_data)[0]
            st.success(f"Predicted Sustainability Score: {result: .2f}")
        # score = model.predict(input_data)[0]
        # st.markdown(f"Predicted Sustainability Score: {score: .2f}")
        # if result < 60:
        #     st.warning("Consider reducing fertilizer/pesticide usage for better Sustainability")
        # else:
        #     st.info("You're on the right track! Maintain eco-friendly practices")

            insights = []
            if result >= 75:
                st.success("Excellent! Your Farming practice is highly sustainable")
                st.info("Keep using eco-friendly methods.\n Consider organic pest control.\n Maintain soil pH between 6.0-7.0")
            elif result >= 50:
                st.warning("Moderate Sustainability. You may want to reduce chemical usage")
                st.info("Reduce pesticide usage if possible.\n Check irrigation frequency.\n Try Crop rotation")
            else:
                st.error("Low Sustainability. Urgent improvement needed")
                st.info("Consider switching to organic fertilizers.\n Reduce chemical inputs.\n Optimize water usage.\n Get soil tested")


            if fertilizer_usage > 80:
                st.warning("High fertilizer usage detected.Consider reducing to prevent soil degradation")
            elif fertilizer_usage < 30:
                st.info("Fertilizer usage is within an eco-friendly range")

            if pesticide_usage > 20:
                st.warning("Excessive pesticide use detected. Use biopesticides if possible")   
            elif pesticide_usage < 5:
                st.info("Minimal pesticide use! Great for long-term soil and crop health") 

            if soil_pH < 5.5:
                st.warning("Soil is too acidic. Consider using lime to balance pH")
            elif soil_pH > 7.5:
               st.warning("Soil is too alkaline. Add organic compost or sulfur to reduce pH")

            if soil_moisture < 15:
               st.warning("Low soil moisture. Efficient irrigation or mulching might help retain water")            


            st.progress(min(int(result), 100))
            st.subheader("Resource Usage Breakdown")
            resource_df = pd.DataFrame({
              'Resource': ['Fertilizer (Kg)', 'Pesticide (Kg)'],
               'Usage': [fertilizer_usage, pesticide_usage]
        })
            st.bar_chart(resource_df.set_index('Resource'))  

            input_data['Predicted_Score'] = result
            csv = input_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Report (CSV)",
                data=csv,
                file_name='sustainability_report.csv',
                mime='text/csv'
            )  

            inputs = {
                'Soil pH' : soil_pH,
                'Temperature (°C)' : temperature,
                'Soil Moisture': soil_moisture,
                'Rainfall (mm)': rainfall,
                'Crop Tye': crop_type,
                'Fertilizer Usage (Kg)': fertilizer_usage,
                'Pesticide Usage (Kg)': pesticide_usage,
                'Crop Yield (ton)': crop_yield 
    
            }
            pdf_bytes = generate_pdf(result, insights, inputs)
            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            href= f'<a href="data:application/pdf;base64,{b64_pdf}" download="sustainability_report.pdf"> Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)      
        except Exception as e:
            st.error(f"Error: {e}")   
elif page == "Tips":
    st.title("Sustainable Agriculture Tips")
    st.markdown("<br>", unsafe_allow_html=True)
    tips = [
        "Use organic fertilizers where possible.",
        "Optimize irrigation to conserve water.",
        "Practice crop rotation to maintain soil health.",
        "Minimize pesticide use and consider biopesticides.",
        "Use weather forecasts to plan farming schedules.",
    ]
    for text in tips:
        st.markdown(f"- {text}")
     
