"""
Core Cog - الأوامر الأساسية للبوت
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="سرعة البوت")
    async def ping(self, ctx):
        await ctx.reply(f"🏓 {round(self.bot.latency*1000)}ms", mention_author=False)

    @commands.hybrid_command(name="bot", description="معلومات البوت")
    async def botinfo(self, ctx):
        embed = discord.Embed(title="🤖 MAX BOT", color=0x6366f1)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency*1000)}ms")
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)))
        embed.add_field(name="Uptime", value=str(discord.utils.utcnow() - self.bot.start_time).split('.')[0])
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="server", description="معلومات السيرفر")
    async def server(self, ctx):
        embed = discord.Embed(title=f"🌐 {ctx.guild.name}", color=0x6366f1)
        embed.add_field(name="Members", value=str(ctx.guild.member_count))
        embed.add_field(name="Channels", value=str(len(ctx.guild.channels)))
        embed.add_field(name="Roles", value=str(len(ctx.guild.roles)))
        embed.add_field(name="Owner", value=str(ctx.guild.owner))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="userinfo", description="معلومات عضو")
    @app_commands.describe(member="العضو")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member.name}", color=0x6366f1)
        embed.add_field(name="ID", value=str(member.id))
        embed.add_field(name="Joined", value=str(member.joined_at)[:10] if member.joined_at else "?")
        embed.add_field(name="Created", value=str(member.created_at)[:10])
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="avatar", description="صورة عضو")
    @app_commands.describe(member="العضو")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🖼️ {member.name}", color=0x6366f1)
        embed.set_image(url=member.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="health", description="صحة البوت")
    async def health(self, ctx):
        embed = discord.Embed(title="🩺 صحة البوت", color=0x10b981)
        embed.add_field(name="Status", value="✅ Online")
        embed.add_field(name="Ping", value=f"{round(self.bot.latency*1000)}ms")
        embed.add_field(name="DB", value="✅ Connected")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="settings", description="عرض الإعدادات")
    async def settings(self, ctx):
        embed = discord.Embed(title="⚙️ إعدادات السيرفر", color=0x6366f1)
        embed.add_field(name="Dashboard", value="[فتح لوحة التحكم](https://web-production-f6fb8.up.railway.app)")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name="clear", aliases=["c", "مسح"], description="مسح رسائل")
    @app_commands.describe(amount="العدد من 1 إلى 100")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx, amount: commands.Range[int, 1, 100] = 10):
        await ctx.defer(ephemeral=True)
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 تم مسح {len(deleted)} رسالة", ephemeral=True)

    @commands.hybrid_command(name="lock", description="قفل القناة")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.reply("🔒 تم قفل القناة", mention_author=False)

    @commands.hybrid_command(name="unlock", description="فتح القناة")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.reply("🔓 تم فتح القناة", mention_author=False)

    @commands.hybrid_command(name="kick", description="طرد عضو")
    @app_commands.describe(member="العضو", reason="السبب")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await ctx.reply(f"👢 تم طرد {member.mention}", mention_author=False)

    @commands.hybrid_command(name="ban", description="حظر عضو")
    @app_commands.describe(member="العضو", reason="السبب")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await ctx.reply(f"🔨 تم حظر {member.mention}", mention_author=False)

    @commands.hybrid_command(name="timeout", description="كتم عضو")
    @app_commands.describe(member="العضو", duration="بالثواني", reason="السبب")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: int = 60, reason: str = None):
        await member.timeout(discord.utils.utcnow() + timedelta(seconds=duration), reason=reason)
        await ctx.reply(f"🔇 تم كتم {member.mention} لمدة {duration} ثانية", mention_author=False)


async def setup(bot):
    await bot.add_cog(Core(bot))
