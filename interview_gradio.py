import os
import google.generativeai as genai
import gradio as gr
import pyaudio
import wave
import json
import numpy as np
import torch
from transformers import pipeline

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GENAI_API_KEY", ""))

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# VTTAI API details (replace with your actual API key)
# VTT_API_KEY = os.getenv("VTT_API_KEY", "")
# VTT_STT_URL = 'https://viettelai.vn/asr/recognize'
# Initialize PhoWhisper
transcriber = pipeline(
    "automatic-speech-recognition",
    model="vinai/PhoWhisper-small",
    device="cuda" if torch.cuda.is_available() else "cpu"
)
# PyAudio settings for microphone input
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 5  # Duration for each recorded chunk
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks
FORMAT = pyaudio.paInt16
CHANNELS = 1
MAX_RECORD_SECONDS = 60  # Maximum recording duration
SILENCE_THRESHOLD = 500  # Adjust this value based on your microphone and environment
SILENCE_DURATION = 5 

HR_PROMPT = """Bạn sẽ đóng vai một nhà tuyển dụng tại một công ty công nghệ lớn. Nhiệm vụ của bạn là phỏng vấn tôi cho vị trí [vị trí ứng tuyển, ví dụ: Kỹ sư phần mềm]. Bạn sẽ đặt những câu hỏi từ danh sách dưới đây, và chỉ dừng lại khi cảm thấy đã có đủ thông tin để đưa ra đánh giá về khả năng của tôi cho vị trí này.
Danh sách câu hỏi phỏng vấn:
1. Bạn đã có tìm hiểu gì về công ty không?
2. Tại sao bạn nghỉ việc ở công ty cũ?
3. Vì sao bạn hứng thú với vị trí này?
4. Vì sao bạn lại muốn làm việc ở đây?
5. Thế mạnh lớn nhất của bạn trong công việc là gì?
6. Làm thế nào để bạn xử lý xung đột tại nơi làm việc?
7. Bạn định nghĩa “làm việc chăm chỉ” là như thế nào?
8. Bạn đánh giá thành công của mình như thế nào?
9. Mô tả quyết định lớn nhất mà bạn đã đưa ra trong sự nghiệp của mình.
10. Bạn hiểu văn hóa của chúng tôi như thế nào?
11. Bạn đã từng gặp thất bại trong công việc chưa? Bạn đã học được gì từ trải nghiệm đó và áp dụng nó như thế nào trong công việc sau này?
12. Hãy mô tả một tình huống mà bạn phải đưa ra quyết định khó khăn với thông tin hạn chế. Cách tiếp cận của bạn là gì và kết quả ra sao?
13. Bạn có thể chia sẻ về một người lãnh đạo hoặc người cố vấn mà bạn ngưỡng mộ và lý do tại sao?
14. Hãy kể về một lần bạn phải hợp tác với một nhóm người có quan điểm và cách làm việc khác biệt. Bạn đã làm gì để đạt được mục tiêu chung?
15. Nếu phát hiện đồng nghiệp vi phạm nội quy công ty, bạn sẽ làm gì?
16. Nếu như được giao một công việc có deadline quá gấp, bạn sẽ làm gì?
17. Bạn có thường hay lên kế hoạch cho mình trong tương lai không? Bạn áp dụng việc lên kế hoạch cho công việc như thế nào?
18. Bạn vẫn chưa xử lý hết công việc của bản thân nhưng đồng nghiệp lại nhờ bạn xử lý giúp công việc của họ? Bạn sẽ làm gì?
19. Bạn sẽ làm gì khi đã hết giờ làm nhưng đồng nghiệp vẫn chưa đứng dậy ra về?
Yêu cầu:
* Bạn có thể chọn ngẫu nhiên bất kỳ câu hỏi nào từ danh sách trên để hỏi tôi.
* Sau mỗi câu trả lời của tôi, bạn có thể đưa ra nhận xét ngắn hoặc tiếp tục với câu hỏi khác.
* Khi cảm thấy đã đủ thông tin, hãy đưa ra đánh giá tổng thể về tôi và cho biết liệu tôi có phù hợp với vị trí này không.
Cách sử dụng:
* Người dùng sẽ trả lời từng câu hỏi từ AI (nhà tuyển dụng).
* AI sẽ tiếp tục đặt câu hỏi hoặc đưa ra nhận xét dựa trên câu trả lời của người dùng cho đến khi nó cho rằng đã đủ thông tin để đưa ra đánh giá."""
GREETING_TEMPLATE = """Xin chào, rất vui được gặp bạn! Tôi là [tên HR], đại diện của [tên công ty] hôm nay. Cảm ơn bạn đã dành thời gian tham gia buổi phỏng vấn cho vị trí [vị trí].
Để bắt đầu, bạn có thể chia sẻ một chút về bản thân và lý do bạn muốn ứng tuyển vào vị trí này tại [tên công ty] không?"""
# Quay man hinh bang javascript (chua hoan thanh)
screen_record_js = """
<script>
console.log('Screen recording script loaded');

(function() {
  var mediaRecorder;
  var recordedChunks = [];

  function startScreenRecording() {
    console.log('Attempting to start screen recording');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
      console.error('Screen capture not supported in this browser');
      return;
    }

    navigator.mediaDevices.getDisplayMedia({ video: true })
      .then(function(stream) {
        console.log('Screen capture stream obtained');
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = function(event) {
          console.log('Data available event fired');
          if (event.data.size > 0) {
            recordedChunks.push(event.data);
          }
        };

        mediaRecorder.onstop = function() {
          console.log('MediaRecorder stopped, processing video');
          var blob = new Blob(recordedChunks, { type: 'video/webm' });
          var url = URL.createObjectURL(blob);
          var a = document.createElement('a');
          document.body.appendChild(a);
          a.style.display = 'none';
          a.href = url;
          a.download = 'interview-recording.webm';
          a.click();
          window.URL.revokeObjectURL(url);
          console.log('Video download initiated');
        };

        mediaRecorder.start();
        console.log('MediaRecorder started');
      })
      .catch(function(error) {
        console.error("Error accessing screen capture:", error);
      });
  }

  function stopScreenRecording() {
    console.log('Attempting to stop screen recording');
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(function(track) { track.stop(); });
      console.log('Screen recording stopped');
    } else {
      console.log('MediaRecorder not active, nothing to stop');
    }
  }

  // Start recording when the page loads
  window.addEventListener('load', function() {
    console.log('Page loaded, starting screen recording');
    startScreenRecording();
  });

  // Stop recording when the "End Interview" button is clicked
  document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up End Interview button listener');
    var endInterviewButton = document.getElementById('end-interview-button');
    if (endInterviewButton) {
      endInterviewButton.addEventListener('click', function() {
        console.log('End Interview button clicked');
        stopScreenRecording();
      });
    } else {
      console.error('End Interview button not found');
    }
  });
})();
</script>
"""
# Job Description Template
JOB_DESCRIPTION = """
VỊ TRÍ: [position]
CÔNG TY: [company_name]

MÔ TẢ CÔNG VIỆC:
- Phát triển và duy trì các ứng dụng phần mềm theo yêu cầu của dự án
- Tham gia vào quá trình thiết kế, coding, testing và debugging
- Làm việc trong môi trường Agile/Scrum
- Cộng tác với các thành viên khác trong team

YÊU CẦU:
1. Kinh nghiệm:
   - Tối thiểu 2 năm kinh nghiệm phát triển phần mềm
   - Kinh nghiệm với các framework hiện đại

2. Kỹ năng kỹ thuật:
   - Thành thạo các ngôn ngữ lập trình: Python, JavaScript
   - Kinh nghiệm với cơ sở dữ liệu
   - Hiểu biết về REST API

3. Kỹ năng mềm:
   - Kỹ năng giao tiếp tốt
   - Khả năng làm việc nhóm
   - Tư duy giải quyết vấn đề

4. Yêu cầu khác:
   - Tiếng Anh giao tiếp tốt
   - Khả năng học hỏi nhanh
   - Tinh thần trách nhiệm cao

QUYỀN LỢI:
- Mức lương cạnh tranh
- Chế độ bảo hiểm đầy đủ
- Môi trường làm việc chuyên nghiệp
- Cơ hội học hỏi và phát triển
"""

# Chat History 
chat_history = []
# def analyze_interview_responses(chat_log):
#     """
#     Phân tích chi tiết các câu trả lời trong buổi phỏng vấn
#     """
#     analysis_prompt = f"""Dựa trên cuộc phỏng vấn sau, hãy phân tích chi tiết từng câu trả lời của ứng viên:

#     {format_chat_for_analysis(chat_log)}

#     Hiển thị câu hỏi và câu trả lời theo thứ tự.

#     Vui lòng đánh giá:

#     1. CHẤT LƯỢNG CÂU TRẢ LỜI
#     - Độ phù hợp với câu hỏi (/10)
#     - Độ chi tiết và đầy đủ (/10)
#     - Tính thuyết phục (/10)
#     - Khả năng đưa ra ví dụ cụ thể (/10)

#     2. KỸ NĂNG GIAO TIẾP
#     - Cách trình bày mạch lạc (/10) 
#     - Mức độ sử dụng từ đệm (càng ít càng tốt) (/10)
#     - Tốc độ và sự trôi chảy (/10)
#     - Sự tự tin (/10)

#     3. PHÂN TÍCH CHI TIẾT
#     - Điểm mạnh nổi bật:
#     - Điểm cần cải thiện:
#     - Mức độ phù hợp với vị trí (/10):

#     4. NHẬN XÉT
#     - Tổng quan:
#     - Đánh giá cuối cùng:
#     """

#     try:
#         response = model.generate_content(analysis_prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Error generating analysis: {str(e)}"

def analyze_interview_responses(chat_log):
                         
    analysis_prompt = f"""Phân tích chi tiết các câu trả lời trong buổi phỏng vấn và cung cấp đầu ra JSON (if no strengths put "Không có" to the list) vơi cấu trúc sau::
    {{
        "response_quality": {{
            "relevance": số nguyên 1-10,
            "completeness": số nguyên 1-10,
            "persuasiveness": số nguyên 1-10,
            "examples": số nguyên 1-10
        }},
        "communication": {{
            "clarity": số nguyên 1-10,
            "filler_words": số nguyên 1-10,
            "fluency": số nguyên 1-10,
            "confidence": số nguyên 1-10
        }},
        "evaluation": {{
            "strengths": [danh sách điểm mạnh],
            "fit_score": số nguyên 1-10,
            "comments": "bình luận cuối cùng"
        }}
    }}
    
    Interview transcript:
    {format_chat_for_analysis(chat_log)}
    """
    
    try:
        response = model.generate_content(analysis_prompt)
        response_text = response.text.strip()
        
        # Remove markdown code block if present
        if response_text.startswith('```'):
            response_text = response_text.replace('```json\n', '', 1)
            response_text = response_text.replace('\n```', '', 1)
            
        # Clean up any remaining whitespace
        response_text = response_text.strip()
        
        return json.loads(response_text)
    except Exception as e:
        return {
            "response_quality": {"relevance": 0, "completeness": 0, "persuasiveness": 0, "examples": 0},
            "communication": {"clarity": 0, "filler_words": 0, "fluency": 0, "confidence": 0},
            "evaluation": {
                "strengths": [f"Error generating analysis: {str(e)}"],
                "improvements": [f"Error generating analysis: {str(e)}"],
                "fit_score": 0,
                "comments": f"Error generating analysis: {str(e)}"
            }
        }

def format_chat_for_analysis(chat_log):
    """
    Format lịch sử chat để phân tích
    """
    formatted_chat = []
    for entry in chat_log:
        if entry["role"] == "assistant":
            formatted_chat.append(f"Câu hỏi: {entry['content']}")
        elif entry["role"] == "user":
            formatted_chat.append(f"Trả lời: {entry['content']}")
    return "\n\n".join(formatted_chat)

def process_audio(audio_input, chat_log):
    new_visible_chat, new_chat_log, audio_update = respond(audio_input, chat_log)
    status = "" if new_visible_chat else "Không thể xử lý âm thanh. Vui lòng thử lại."
    return new_visible_chat, new_chat_log, audio_update, status

def record_audio(filename="temp_audio.wav"):
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                                  input=True, frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0
    print("Recording audio...")

    for _ in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

        audio_data = np.frombuffer(data, dtype=np.int16)
        if np.abs(audio_data).mean() < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0
        if silent_chunks > SILENCE_DURATION * (RATE / CHUNK):
            print("Silence detected, stopping recording.")
            break

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio_phowhisper(filename="temp_audio.wav"):
    try:
        # Read the audio file
        import soundfile as sf
        audio, sr = sf.read(filename)
        
        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # Convert to float32 and normalize
        audio = audio.astype(np.float32)
        if audio.max() > 1.0:
            audio = audio / 32768.0
            
        # Transcribe
        result = transcriber({"sampling_rate": sr, "raw": audio})
        transcription = result["text"].strip()
        
        return transcription
    except Exception as e:
        return f"Error in transcription: {str(e)}"

def initialize_chat(hr_name, company_name, position):
    greeting = GREETING_TEMPLATE.replace('[tên HR]', hr_name)
    greeting = greeting.replace('[tên công ty]', company_name)
    greeting = greeting.replace('[vị trí]', position)
    
    chat_log = [
        {"role": "system", "content": HR_PROMPT},
        {"role": "assistant", "content": greeting}
    ]
    return [("AI", greeting)], chat_log

def chat_interviewer(user_input, chat_log):
    if not user_input and len(chat_log) == 2:  # System message and greeting present
        return chat_log[1]["content"], chat_log
    
    chat_log.append({"role": "user", "content": user_input})
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in chat_log]) + "\nHR:"

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith("Assistant:"):
            response_text = response_text[len("Assistant:"):].strip()
        chat_log.append({"role": "assistant", "content": response_text})
        return response_text, chat_log
    except Exception as e:
        return f"Error generating response: {str(e)}", chat_log

def respond(audio_input, chat_log):
    try:
        if not audio_input:
            # Include only non-system messages
            visible_chat_log = [(content, "") for role, content in chat_log if role != "system"]
            return visible_chat_log, chat_log, gr.update(visible=True)

        user_response = transcribe_audio_phowhisper(filename=audio_input)

        if "Error in transcription" in user_response:
            visible_chat_log = [(content, "") for role, content in chat_log if role != "system"]
            return visible_chat_log, chat_log, gr.update(visible=True)

        ai_response, new_chat_log = chat_interviewer(user_response, chat_log)
        
        # Create Q&A pairs and include standalone assistant messages
        visible_chat_log = []
        i = 0
        while i < len(new_chat_log):
            role = new_chat_log[i]["role"]
            content = new_chat_log[i]["content"]
            
            if role == "assistant":
                # Check if the assistant message is not part of a Q&A pair
                if i == 0 or new_chat_log[i-1]["role"] != "user":
                    visible_chat_log.append(("", content))
            elif role == "user":
                # Pair with the next assistant message if available
                if i + 1 < len(new_chat_log) and new_chat_log[i + 1]["role"] == "assistant":
                    assistant_content = new_chat_log[i + 1]["content"]
                    visible_chat_log.append((content, assistant_content))
                    i += 1  # Skip the next message as it's already paired
                else:
                    visible_chat_log.append((content, ""))
            i += 1

        return visible_chat_log, new_chat_log, gr.update(visible=True)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        visible_chat_log = [(content, "") for role, content in chat_log if role != "system"]
        return visible_chat_log, chat_log, gr.update(visible=True)
def end_interview(chat_log):
    # Generate both overview and detailed analysis
    overview = generate_candidate_overview(chat_log)
    detailed_analysis = analyze_interview_responses(chat_log)
    
    # Create JSON structure
    report_json = {
        "candidate_report": {
            "overview": {
                "strengths": overview["strengths"],
                "weaknesses": overview["weaknesses"],
                "overall_fit_score": overview["fit_score"]
            },
            "detailed_analysis": {
                "response_quality": {
                    "relevance_score": detailed_analysis["response_quality"]["relevance"],
                    "completeness_score": detailed_analysis["response_quality"]["completeness"],
                    "persuasiveness_score": detailed_analysis["response_quality"]["persuasiveness"],
                    "examples_score": detailed_analysis["response_quality"]["examples"]
                },
                "communication_skills": {
                    "clarity_score": detailed_analysis["communication"]["clarity"],
                    "filler_words_score": detailed_analysis["communication"]["filler_words"],
                    "fluency_score": detailed_analysis["communication"]["fluency"],
                    "confidence_score": detailed_analysis["communication"]["confidence"]
                },
                "final_evaluation": {
                    "key_strengths": detailed_analysis["evaluation"]["strengths"],
                    "position_fit_score": detailed_analysis["evaluation"]["fit_score"],
                    "final_comments": detailed_analysis["evaluation"]["comments"]
                }
            }
        }
    }
    
    # Save the JSON report
    try:
        with open("interview_report.json", "w", encoding="utf-8") as file:
            json.dump(report_json, file, ensure_ascii=False, indent=2)
        save_status = "Interview report saved successfully."
    except Exception as e:
        save_status = f"Error saving report: {str(e)}"
    
    return report_json, save_status

def generate_candidate_overview(chat_log):
        chat_history = "\n".join([f"Q: {entry['content']}" if entry["role"] == "assistant" else f"A: {entry['content']}"
                                for entry in chat_log if entry["role"] != "system"])
                              
        summary_prompt = f"""Đánh giá đoạn phỏng vấn sau và cung cấp một đầu ra JSON (if no strengths or weaknesses put "Không có" to the list) với cấu trúc sau::
        {{
            "strengths": [danh sách điểm mạnh],
            "weaknesses": [danh sách điểm yếu],
            "fit_score": số nguyên 1-10
        }}
        
        Đoạn phỏng vấn:
        {chat_history}
        """
        
        try:
            response = model.generate_content(summary_prompt)
            response_text = response.text.strip()
        
            # Remove markdown code block if present
            if response_text.startswith('```'):
                response_text = response_text.replace('```json\n', '', 1)
                response_text = response_text.replace('\n```', '', 1)
            
            # Clean up any remaining whitespace
            response_text = response_text.strip()
            
            return json.loads(response_text)

        except Exception as e:
            return {
                "strengths": [f"Error generating strengths: {str(e)}"],
                "weaknesses": [f"Error generating weaknesses: {str(e)}"],
                "fit_score": 0
            }

# def save_transcript(chat_log):
#     transcript = "\n".join([f"{entry['role']}: {entry['content']}" for entry in chat_log if entry["role"] != "system"])
#     try:
#         with open("interview_transcript.txt", "w", encoding="utf-8") as file:
#             file.write(transcript)
#         return "Chat transcript saved successfully."
#     except Exception as e:
#         return f"Error saving transcript: {str(e)}"
def video_identity(video):
    return video
# Gradio UI 
custom_css = """
#left-column {
    width: 50%;
    float: left;
}

#right-column {
    width: 50%;
    float: right;
}

.chatbot-container {
    height: 500px;
    overflow-y: auto;
}
"""

# Gradio UI
with gr.Blocks(css=custom_css , theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate")) as interface:
    gr.Markdown("# AI interview (Vietnamese)")

    with gr.Row():
        with gr.Column(scale=1, elem_id="left-column"):
            video_input = gr.Video(label="Record your video")  # Video input on the left side

        with gr.Column(scale=1, elem_id="right-column"):
            chatbot = gr.Chatbot(label="Chat", elem_classes="chatbot-container", height=400)  # Chatbot on the right side
            audio_input = gr.Audio(type="filepath", label="Speak Your Message")
            status_message = gr.Markdown("")
            candidate_overview = gr.TextArea(
            placeholder="Detailed interview analysis will appear here", 
            label="Interview Analysis",
            visible=False,
            lines=20
            )
            respond_button = gr.Button("Respond")  # Respond Button
            end_interview_button = gr.Button("End Interview", elem_id="end-interview-button")


    hr_name = "Nguyễn Văn A"
    company_name = "Công ty XYZ"
    position = "Kỹ sư phần mềm"

    initial_chat, initial_state = initialize_chat(hr_name, company_name, position)
    state = gr.State(initial_state)

    # def generate_candidate_overview(chat_log):
    #     """
    #     Tạo tổng quan về hiệu suất của ứng viên sử dụng lịch sử trò chuyện.
    #     """
    #     chat_history = "\n".join([f"Q: {entry['content']}" if entry["role"] == "assistant" else f"A: {entry['content']}"
    #                               for entry in chat_log if entry["role"] != "system"])

    #     summary_prompt = f"""Dựa trên cuộc trò chuyện phỏng vấn sau đây, hãy cung cấp một tổng quan chi tiết về điểm mạnh, điểm yếu của ứng viên và liệu họ có phù hợp với vị trí này trên thang điểm 1-10 hay không.:

    #     {chat_history}

    #     Vui lòng tóm tắt hiệu suất của ứng viên."""

    #     try:
    #         response = model.generate_content(summary_prompt)
    #         candidate_overview = response.text.strip()
    #         return candidate_overview
    #     except Exception as e:
    #         return f"Error generating summary: {str(e)}"

    

    # txt version
    # def end_interview(chat_log):
    #     # Generate both overview and detailed analysis
    #     overview = generate_candidate_overview(chat_log)
    #     detailed_analysis = analyze_interview_responses(chat_log)
        
    #     # Combine results
    #     full_report = f"""
    #     TỔNG QUAN ỨNG VIÊN
    #     ==================
    #     {overview}

    #     PHÂN TÍCH CHI TIẾT
    #     ==================
    #     {detailed_analysis}
    #     """
        
    #     # Save the full report
    #     try:
    #         with open("interview_report.txt", "w", encoding="utf-8") as file:
    #             file.write(full_report)
    #         save_status = "Interview report saved successfully."
    #     except Exception as e:
    #         save_status = f"Error saving report: {str(e)}"
        
    #     return full_report, save_status



    # k su dung
    # def save_overview(overview):
    #     try:
    #         with open("candidate_overview.txt", "w", encoding="utf-8") as file:
    #             file.write(overview)
    #         return "Candidate overview saved successfully."
    #     except Exception as e:
    #         return f"Error saving overview: {str(e)}"
    def process_video(video_input):
                # Video processing logic
                return "Video captured successfully"

    respond_button.click(fn=process_audio, inputs=[audio_input, state], outputs=[chatbot, state, audio_input, status_message])
    respond_button.click(fn=process_video, inputs=[video_input], outputs=[status_message])

    end_interview_button.click(fn=end_interview, inputs=[state], outputs=[candidate_overview, status_message])
    # Set initial chat state
    chatbot.value = initial_chat

    #interface.load(None, None, js= screen_record_js)
interface.launch(share=True)
#record whole screen and save as video

