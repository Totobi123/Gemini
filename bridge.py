
import asyncio

import os

import logging

import json

from telegram import Update

from telegram.ext import Application, MessageHandler, filters, ContextTypes



# Setup logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)



TOKEN = "8655041916:AAEwuN33mNcd1SqToflIzqp5bT_Ikdvv3cY"

WORKING_DIR = "/root/gemini-bridge"



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text or update.message.caption

    if not user_text: return



    status_msg = await update.message.reply_text("🛰️ Buddy is processing... [Streaming Mode]")



    try:

        # Using --output-format stream-json to capture "thoughts" and "calls"

        cmd = [

            'gemini', 

            '--yolo', 

            '--output-format', 'stream-json',

            '-p', f"@{WORKING_DIR}/GEMINI.md {user_text}"

        ]



        process = await asyncio.create_subprocess_exec(

            *cmd,

            stdout=asyncio.subprocess.PIPE,

            stderr=asyncio.subprocess.PIPE,

            cwd=WORKING_DIR

        )



        full_summary = ""

        

        # Read the stdout line by line as it streams

        while True:

            line = await process.stdout.readline()

            if not line:

                break

            

            try:

                data = json.loads(line.decode().strip())

                

                # If Gemini is "thinking", send that thought to Telegram

                if "thought" in data:

                    thought_text = data["thought"]

                    # We only send a snippet if it's too long, to avoid flooding

                    await update.message.reply_text(f"🤔 *Thought:* {thought_text[:500]}...", parse_mode='Markdown')

                

                # If Gemini is calling a tool (like curl or ls)

                if "call" in data:

                    tool_name = data["call"].get("tool", "unknown")

                    await update.message.reply_text(f"🛠️ *Action:* Executing {tool_name}...")



                # If we get final content

                if "content" in data:

                    full_summary += data["content"]



            except json.JSONDecodeError:

                # If it's not JSON (e.g., standard text), just append it

                full_summary += line.decode()



        # Catch any errors from stderr

        stdout, stderr = await process.communicate()

        error_output = stderr.decode().strip()



        final_output = full_summary + "\n" + error_output

        if not final_output.strip():

            final_output = "Mission complete. No data returned."



        # Send the final compiled results

        await update.message.reply_text(f"🏁 *Final Results & Summary:*\n\n{final_output[:3500]}", parse_mode='Markdown')



    except Exception as e:

        logger.error(f"Bridge Error: {e}")

        await update.message.reply_text(f"❌ Bridge Error: {str(e)}")



def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bridge started.")

    app.run_polling(drop_pending_updates=True)



if __name__ == "__main__":

    main()

