import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from src.rag import RAGPipeline

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)
rag = RAGPipeline()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    rag.build_index()
    print("Knowledge base indexed and ready.")


@bot.command(name="ask")
async def ask(ctx, *, query: str = None):
    if not query:
        await ctx.send("Please provide a question. Usage: `/ask <your question>`")
        return

    async with ctx.typing():
        answer, sources = rag.query(query)

    embed = discord.Embed(description=answer, color=discord.Color.blue())
    embed.set_author(name="RAG Bot")
    embed.set_footer(text=f"Sources: {sources}")
    await ctx.send(embed=embed)


@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.green())
    embed.add_field(name="/ask <question>", value="Ask a question from the knowledge base.", inline=False)
    embed.add_field(name="/help", value="Show this help message.", inline=False)
    embed.add_field(name="/sources", value="List available knowledge base documents.", inline=False)
    await ctx.send(embed=embed)


@bot.command(name="sources")
async def sources(ctx):
    docs = rag.list_documents()
    embed = discord.Embed(title="Knowledge Base Documents", color=discord.Color.purple())
    for doc in docs:
        embed.add_field(name=doc, value="Available", inline=True)
    await ctx.send(embed=embed)


bot.run(os.getenv("DISCORD_TOKEN"))
