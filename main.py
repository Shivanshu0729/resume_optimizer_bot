import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from file_parser_mod.file_parser import extract_text
from scorer.ats_scorer import score_resume
from optimizer.resume_optimizer import optimize_resume
from renderer.pdf_renderer import render_to_pdf

load_dotenv()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_sessions: dict = {}

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_sessions[uid] = {}
    await update.message.reply_text(
        "*Welcome to ATS Resume Optimizer Bot!*\n\n"
        "I'll analyze your resume against any job description, give you a detailed score, "
        "and generate a professionally optimized version.\n\n"
        "\n"
        "*Step 1:* Paste your Job Description below.\n"
        "*Step 2:* Upload your Resume (PDF, DOCX, or TXT)\n"
        "*Step 3:* Get your ATS Score + Optimized Resume\n"
        "\n\n"
        "Let's start — paste your Job Description now!",
        parse_mode="Markdown"
    )

async def reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_sessions[uid] = {}
    await update.message.reply_text(
        "Session reset! Paste a new Job Description to start fresh."
    )

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " *ATS Resume Bot — Help*\n\n"
        "*/start* — Start a new analysis\n"
        "*/reset* — Clear session and start over\n"
        "*/help* — Show this message\n\n"
        "*Supported file formats:* PDF, DOCX, TXT\n\n"
        "*Score breakdown:*\n"
        "• 75–100 Strong match\n"
        "• 55–74 Partial match\n"
        "• Below 55 Needs major improvement\n\n"
        "After the scan you can request different resume formats:\n"
        "Single Page | Two Page | ATS Plain | Executive",
        parse_mode="Markdown"
    )

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    session = user_sessions.get(uid, {})

    if "jd" not in session:
        user_sessions[uid] = {"jd": update.message.text}
        await update.message.reply_text(
            "*Job Description saved!*\n\n"
            "Now upload your resume file (PDF, DOCX, or TXT) 📎",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "📎 Please upload your resume file now.\n"
            "Use /reset to start over with a new JD."
        )

async def handle_file(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    session = user_sessions.get(uid, {})

    if "jd" not in session:
        await update.message.reply_text(
            "Please paste your Job Description first, then upload your resume.\n"
            "Use /start to begin."
        )
        return

    processing_msg = await update.message.reply_text(
        "*Processing your resume...*\n\n"
        "Parsing document...\n"
        "Running ATS analysis...\n"
        "Generating optimized version...\n\n"
        "_This takes about 20–30 seconds_",
        parse_mode="Markdown"
    )

    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    os.makedirs("output", exist_ok=True)
    file_path = f"output/{uid}_{file_name}"
    await file.download_to_drive(file_path)

    try:
        resume_text = extract_text(file_path)
        jd_text = session["jd"]

        result = score_resume(resume_text, jd_text)
        score = result["total_score"]
        gaps = result.get("missing_keywords", [])
        gap_msg = result.get("gap_message", "")
        is_match = result.get("is_good_match", False)

        optimized = optimize_resume(resume_text, jd_text, gaps)
        user_sessions[uid]["optimized"] = optimized
        user_sessions[uid]["score_result"] = result

        pdf_path = render_to_pdf(optimized, f"output/{uid}_optimized.pdf", template="single_page")

        if score >= 75:
            status_emoji = "✅"
            status_text = "Strong Match"
            bar = "🟩🟩🟩🟩🟩🟩🟩🟩"
        elif score >= 55:
            status_emoji = "⚠️"
            status_text = "Partial Match"
            bar = "🟩🟩🟩🟩🟩🟨🟨⬜"
        else:
            status_emoji = "❌"
            status_text = "Needs Improvement"
            bar = "🟩🟩🟥🟥🟥🟥🟥🟥"

        report = (
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"*ATS ANALYSIS REPORT*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{status_emoji} *Status:* {status_text}\n"
            f"*Overall Score:* `{score}/100`\n"
            f"{bar}\n\n"
            f"*Score Breakdown:*\n"
            f"• Keyword Match: `{result.get('keyword_score', 'N/A')}/100`\n"
            f"• Role Alignment: `{result.get('role_alignment_score', 'N/A')}/100`\n"
            f"• Format Score: `{result.get('format_score', 'N/A')}/100`\n\n"
        )

        if not is_match:
            report += f"*Gap Analysis:*\n_{gap_msg}_\n\n"
            if gaps:
                report += f"*Missing Keywords:*\n`{', '.join(gaps[:8])}`\n\n"

        report += (
            f" \n"
            f"*Optimized resume attached below!*\n"
            f"Choose a format variant:"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Single Page", callback_data="fmt_single"),
                InlineKeyboardButton("Two Page", callback_data="fmt_two"),
            ],
            [
                InlineKeyboardButton("ATS Plain", callback_data="fmt_ats"),
                InlineKeyboardButton("Executive", callback_data="fmt_exec"),
            ]
        ])

        await processing_msg.delete()
        await update.message.reply_text(report, parse_mode="Markdown", reply_markup=keyboard)
        await update.message.reply_document(
            document=open(pdf_path, "rb"),
            filename="optimized_resume.pdf",
            caption="Your optimized resume (Single Page format)"
        )

    except Exception as e:
        logger.error(f"Pipeline error for user {uid}: {e}")
        await processing_msg.delete()
        await update.message.reply_text(
            f"*Something went wrong:*\n`{str(e)}`\n\n"
            "Please try /reset and try again.",
            parse_mode="Markdown"
        )

async def handle_format_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    session = user_sessions.get(uid, {})
    optimized = session.get("optimized")

    if not optimized:
        await query.message.reply_text("Please run a scan first with /start.")
        return

    fmt_map = {
        "fmt_single": ("single_page", "Single Page"),
        "fmt_two":    ("two_page",    "Two Page"),
        "fmt_ats":    ("ats_plain",   "ATS Plain"),
        "fmt_exec":   ("executive",   "Executive"),
    }
    template_key, label = fmt_map.get(query.data, ("single_page", "Single Page"))

    await query.message.reply_text(f"Generating *{label}* format...", parse_mode="Markdown")
    pdf_path = render_to_pdf(optimized, f"output/{uid}_optimized_{template_key}.pdf", template=template_key)
    await query.message.reply_document(
        document=open(pdf_path, "rb"),
        filename=f"resume_{template_key}.pdf",
        caption=f"📎 Your resume in *{label}* format",
        parse_mode="Markdown"
    )

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN not found in .env file!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(CallbackQueryHandler(handle_format_button))

    logger.info("ATS Resume Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
