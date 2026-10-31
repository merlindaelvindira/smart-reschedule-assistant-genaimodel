

# 1. SETUP FASTAPI & OPENAPI

app = FastAPI(
    title="Gymnasyum AI - API",
    description="""
    Dokumentasi Smart Reschedule Assistant.
    API ini menangani Intent Classification (Scikit-Learn), Retrieval-Augmented Generation (ChromaDB),
    dan Generative AI Responses (Gemini).
    """,
    version="1.0.0",
    docs_url="/docs",
)

# API Key (Menggunakan Environment Variable di Render, dengan fallback default)
SECRET_API_KEY = os.getenv("API_KEY", "smart_reschedule_assistant_api_key")

def verify_api_key(x_api_key: str = Header(None)):
    """Memeriksa keberadaan dan kecocokan x-api-key di headers."""
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Akses Ditolak: API Key tidak valid!")
    return x_api_key


# 2. SKEMA JSON (OPENAPI SCHEMAS)

# Perbaikan: Mengganti 'example' menjadi 'examples' untuk kompatibilitas Pydantic V2
class ChatRequest(BaseModel):
    sender_id: str = Field(..., examples=["customer_01"], description="ID unik pelanggan dari database web")
    message: str = Field(..., examples=["besok sore saya nggak bisa ikut kelas zumba ya"], description="Pesan chat dari pelanggan")
    available_slots: str = Field(default="", examples=["Sabtu 08:00 WIB"], description="Jadwal slot alternatif dari database")
    action: str = Field(default="process_ai", examples=["process_ai"], description="Pilih 'add_to_buffer' atau 'process_ai'")

class ChatResponseData(BaseModel):
    combined_message: str = Field(..., examples=["besok sore saya nggak bisa ikut kelas zumba ya"])
    predicted_intent: str = Field(..., examples=["Cancel"])
    retrieved_context: str = Field(..., examples=["Kebijakan Pembatalan: ..."])
    ai_draft_response: str = Field(..., examples=["Halo! Kami memahami kondisinya, mari kita jadwalkan ulang..."])

class ChatResponse(BaseModel):
    status: str = Field(default="success", examples=["success"])
    data: ChatResponseData



# 3. ENDPOINT API

@app.post(
    "/api/chat",
    tags=["AI Chat Processing"],
    response_model=ChatResponse,
    summary="Kirim pesan pelanggan ke Pipeline AI",
    description="Menerima pesan chat pelanggan, menganalisis intent, mencari dokumen RAG, dan mengembalikan draft balasan AI."
)
def chat_endpoint(request: ChatRequest, x_api_key: str = Header(..., description="API Key rahasia untuk autentikasi")):
    if x_api_key != BACKEND_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: API Key tidak valid")

    try:
        
        customer_msg, pred_intent, retrieved_ctx, ai_response = process_customer_request(
            sender_id=request.sender_id,
            incoming_bubble=request.message,
            available_slots_str=request.available_slots,
            action=request.action
        )

        return {
            "status": "success",
            "data": {
                "combined_message": customer_msg,
                "predicted_intent": pred_intent,
                "retrieved_context": retrieved_ctx,
                "ai_draft_response": ai_response
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal AI Error: {str(e)}")



# 4. RUNNER UNTUK RENDER

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
