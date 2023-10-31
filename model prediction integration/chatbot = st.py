chatbot = st.toggle("Need help? Click to speak with ChartBot.")

        if chatbot:
     
            openai.api_key = "sk-"
            if "messages" not in st.session_state.keys(): # Initialize the chat messages history
                st.session_state.messages = [
                    {"role": "assistant", "content": "Ask me a question about SmartChart or anything EMS!"}
                ]

            @st.cache_resource(show_spinner=False)
            def load_data():
                with st.spinner(text="Compiling EMS data – hang tight!"):
                    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
                    docs = reader.load_data()
                    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the website you're apart of called SmartChart, which is a patient charting applicaiton for EMTs. Your job is to answer technical questions. Assume that all questions are related to SmartChart and questions about EMS best practices as a whole. Keep your answers technical and based on facts – do not hallucinate features. If a question pertains to a specific protocol or inquiry about what to do in a medical scenario, do not refer to any of SmartChart's features but instead give specific medical advice from the perspective of what a trained EMT should do."))
                    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
                    return index

            index = load_data()
            # chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
            chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

            if prompt := st.chat_input("How does SmartChart work?"): # Prompt for user input and save to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

            for message in st.session_state.messages: # Display the prior chat messages
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # If last message is not from assistant, generate a new response
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = chat_engine.chat(prompt)
                        st.write(response.response)
                        message = {"role": "assistant", "content": response.response}
                        st.session_state.messages.append(message) # Add response to message history

        else:
    
    Purpose

##Make a data/data.md
##Given the high stakes nature of their work, EMTs must optimize the time they have to treat the patient. We came to the conclusion that reducing time spent on patient documentation and protocols can allow EMTs to shift more of their time and focus on actual patient care. To this end, we developed SmartChart, a webapp and deployable machine designed for more efficient and consistent delivery of EMS care.

Innovation
So what problem does SmartChart solve? EMTs are required by law to meticulously record their patient interactions, from vital signs to EMS interventions, and many do so with pen and paper. Not only is this inefficient, but it can also lead to inaccuracies and miscommunication. SmartChart offers a fully virtual solution to this problem, allowing EMTs to log all relevant information into an electronic chart. What makes our application unique is the use of modern technology such as artificial intelligence, computer vision, optical character recognition, and wireless communication to not only save the EMT time on call, but to reduce the chance of malpractice and guide the EMT towards the correct treatment decisions.

Practitioners/Training Requirements + Cost Analysis + Impact on Future Healthcare
Users must be certified EMTs in order to ensure that they have the background knowledge and training necessary to correctly carry-out suggested actions. Our software will be. completely open source and free to use, while the deployable case can be produced for under $150. In the future, we plan to apply for a Small Business Innovation Research (SBIR) grant to further sponsor our production, and get the system in as many ambulance corps as we can.

Home Page:
At the core of SmartChart is the patient charting software that allows the EMT to digitally record patient demographics, vitals, presentation, and medical history, and export the data to whoever is receiving the patient. In order to take vitals more efficiently, we’ve designed the first machine learning model capable of patient documentation through the EMTs voice alone. It intelligently detects and responds to a variety of speech patterns and order, and can process multiple vital inputs at once. Furthermore, if the EMT initially took handwritten notes on the patient and now wants to log it digitally, SmartChart is equipped with optical character recognition that allows for seamless insertion into the chart.

Recommended Actions Page:
In concert with the patient charting page is the recommended actions page, which updates dynamically with the inputted patient information using a novel algorithm tailored for EMS care. With this algorithm, the page will only present protocols for the most likely conditions the patient presents with, allowing patient care to start as soon as possible. If any treatment/medication is contraindicated for the patient given the inputted patient information, the app will notify the EMT within all relevant protocols, reducing the chance of harmful mistakes.

Patient Assessment
In addition to providing fast diagnostics for a patient based on the vitals logged by the EMT, SmartChart also supports diagnostics powered by computer vision. Photos of the patient’s symptoms can be uploaded to the patient assessment tab, and the app will classify the patient's condition using a custom machine learning model trained on common patient presentations, including urticaria, edema, cyanosis, facial drooping, and more. Once the patient presentation is classified, the app will present all of the relevant protocols and information at the EMTs fingertips.

Patient Communication and Transport
To help overcome language barriers, we created the patient communication page, which offers the EMT on-demand translations that can be audio or text-based in 10 different languages. Lastly, the transportation page is designed to alert the EMT about inclement weather conditions in the area and provides a list of the nearest facilities, including hospitals, burn centers, and trauma centers, among others—the inputted patient information is also used to provide a custom facility suggestion tailored to every patient.

DMAC
This is the Deployable Medical Assistance Case or DMAC. Capable of taking patient vitals in real-time and sending them to the SmartChart website for A.I driven processing, the DMAC consists of the processing enclosure, the pulse oximeter finger clip, the temperature probe, and finally, the solar charging system. Inside the processing enclosure is an Adafruit Feather Huzzah V2 Micro controller boasting a fast processor and wifi capability, and a rechargeable LiPo battery. The pulse oximeter finger clip uses a GY-max30102 sensor board to pull the patient's pulse rate and blood oxygen, it also allows for reading human presence. The waterproof DS18b20 temperature probe allows for tracking patient temperature, allowing for important vitals to be sent to the website. There is also a solar charging system using the mcp73871 solar charger controller, which allows for intelligent battery and load charging.
