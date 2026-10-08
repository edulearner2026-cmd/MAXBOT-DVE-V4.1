"""
نظام الترحيب المخصص مع المتغيرات
"""
import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timezone

WELCOME_FILE = "welcome_settings.json"

# المتغيرات المتاحة
AVAILABLE_VARIABLES = {
    "{user}": "اسم المستخدم",
    "{user_mention}": "منشن المستخدم",
    "{user_id}": "أيدي المستخدم",
    "{user_avatar}": "رابط الأفاتار",
    "{user_created}": "تاريخ إنشاء الحساب",
    "{user_joined}": "تاريخ الانضمام",
    "{server_name}": "اسم السيرفر",
    "{server_id}": "أيدي السيرفر",
    "{server_members}": "عدد الأعضاء",
    "{server_icon}": "رابط أيقونة السيرفر",
    "{server_owner}": "مالك السيرفر",
    "{server_created}": "تاريخ إنشاء السيرفر",
    "{member_count}": "عدد الأعضاء الحالي",
    "{boost_count}": "عدد البوستات",
    "{channel_mention}": "منشن القناة",
    "{date}": "التاريخ الحالي",
    "{time}": "الوقت الحالي",
    "{invite_count}": "عدد الدعوات",
    "{role_count}": "عدد الرتب",
    "{emoji_count}": "عدد الإيموجيات",
    "{bot_count}": "عدد البوتات",
    "{human_count}": "عدد البشر",
    "{online_count}": "عدد المتصلين",
    "{offline_count}": "غير المتصلين",
    "{welcome_count}": "عدد الترحيبات",
    "{leave_count}": "عدد المغادرات",
    "{message_count}": "عدد الرسائل",
    "{command_count}": "عدد الأوامر",
    "{uptime}": "وقت تشغيل البوت",
    "{version}": "إصدار البوت",
    "{prefix}": "بادئة الأوامر",
    "{guild_level}": "مستوى السيرفر",
    "{guild_xp}": "خبرة السيرفر",
    "{guild_messages}": "رسائل السيرفر",
    "{guild_joins}": "انضمامات السيرفر",
    "{guild_leaves}": "مغادرات السيرفر",
    "{guild_bans}": "حظرات السيرفر",
    "{guild_kicks}": "طردات السيرفر",
    "{guild_roles}": "رتب السيرفر",
    "{guild_channels}": "قنوات السيرفر",
    "{guild_emojis}": "إيموجيات السيرفر",
    "{guild_boosts}": "بوستات السيرفر",
    "{guild_tier}": "مستوى البوست",
    "{guild_max_members}": "الحد الأقصى للأعضاء",
    "{guild_description}": "وصف السيرفر",
    "{guild_locale}": "لغة السيرفر",
    "{guild_verification}": "مستوى التحقق",
    "{guild_notifications}": "إعدادات الإشعارات",
    "{guild_filter}": "فلتر المحتوى",
    "{guild_2fa}": "التحقق بخطوتين",
    "{guild_mfa}": "المصادقة متعددة العوامل",
    "{guild_explicit}": "فلتر المحتوى الصريح",
    "{guild_nsfw}": "قناة NSFW",
    "{guild_nsfw_level}": "مستوى NSFW",
    "{guild_premium_progress}": "شريط تقدم البوست",
    "{guild_rules_channel}": "قناة القواعد",
    "{guild_updates_channel}": "قناة التحديثات",
    "{guild_system_channel}": "قناة النظام",
    "{guild_afk_channel}": "قناة AFK",
    "{guild_afk_timeout}": "مهلة AFK",
    "{guild_widget}": "ويدجت السيرفر",
    "{guild_widget_channel}": "قناة الويدجت",
    "{guild_partner}": "سيرفر شريك",
    "{guild_verified}": "سيرفر موثق",
    "{guild_vanity}": "رابط مخصص",
    "{guild_banner}": "بانر السيرفر",
    "{guild_splash}": "سبلاش السيرفر",
    "{guild_discovery_splash}": "سبلاش الاكتشاف",
    "{guild_max_presences}": "الحد الأقصى للحضور",
    "{guild_max_channels}": "الحد الأقصى للقنوات",
    "{guild_max_roles}": "الحد الأقصى للرتب",
    "{guild_max_emojis}": "الحد الأقصى للإيموجيات",
    "{guild_max_webhooks}": "الحد الأقصى للويب هوك",
    "{guild_max_integrations}": "الحد الأقصى للتكاملات",
    "{guild_max_invites}": "الحد الأقصى للدعوات",
    "{guild_max_attachments}": "الحد الأقصى للمرفقات",
    "{guild_max_reactions}": "الحد الأقصى للتفاعلات",
    "{guild_max_mentions}": "الحد الأقصى للمنشن",
    "{guild_max_emojis_per_message}": "الحد الأقصى للإيموجيات لكل رسالة",
    "{guild_max_reactions_per_message}": "الحد الأقصى للتفاعلات لكل رسالة",
    "{guild_max_mentions_per_message}": "الحد الأقصى للمنشن لكل رسالة",
    "{guild_max_attachments_per_message}": "الحد الأقصى للمرفقات لكل رسالة",
    "{guild_max_webhooks_per_channel}": "الحد الأقصى للويب هوك لكل قناة",
    "{guild_max_invites_per_channel}": "الحد الأقصى للدعوات لكل قناة",
    "{guild_max_integrations_per_channel}": "الحد الأقصى للتكاملات لكل قناة",
    "{guild_max_emojis_per_channel}": "الحد الأقصى للإيموجيات لكل قناة",
    "{guild_max_roles_per_channel}": "الحد الأقصى للرتب لكل قناة",
    "{guild_max_channels_per_category}": "الحد الأقصى للقنوات لكل تصنيف",
    "{guild_max_categories}": "الحد الأقصى للتصنيفات",
    "{guild_max_threads}": "الحد الأقصى للثريد",
    "{guild_max_thread_members}": "الحد الأقصى لأعضاء الثريد",
    "{guild_max_forum_channels}": "الحد الأقصى لقنوات المنتدى",
    "{guild_max_forum_tags}": "الحد الأقصى لعلامات المنتدى",
    "{guild_max_forum_emojis}": "الحد الأقصى لإيموجيات المنتدى",
    "{guild_max_forum_reactions}": "الحد الأقصى لتفاعلات المنتدى",
    "{guild_max_forum_mentions}": "الحد الأقصى لمنشن المنتدى",
    "{guild_max_forum_attachments}": "الحد الأقصى لمرفقات المنتدى",
    "{guild_max_forum_webhooks}": "الحد الأقصى لويب هوك المنتدى",
    "{guild_max_forum_invites}": "الحد الأقصى لدعوات المنتدى",
    "{guild_max_forum_integrations}": "الحد الأقصى لتكاملات المنتدى",
    "{guild_max_forum_emojis_per_message}": "الحد الأقصى لإيموجيات المنتدى لكل رسالة",
    "{guild_max_forum_reactions_per_message}": "الحد الأقصى لتفاعلات المنتدى لكل رسالة",
    "{guild_max_forum_mentions_per_message}": "الحد الأقصى لمنشن المنتدى لكل رسالة",
    "{guild_max_forum_attachments_per_message}": "الحد الأقصى لمرفقات المنتدى لكل رسالة",
    "{guild_max_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى لكل قناة",
    "{guild_max_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى لكل قناة",
    "{guild_max_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى لكل قناة",
    "{guild_max_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى لكل قناة",
    "{guild_max_forum_roles_per_channel}": "الحد الأقصى لرتب المنتدى لكل قناة",
    "{guild_max_forum_channels_per_category}": "الحد الأقصى لقنوات المنتدى لكل تصنيف",
    "{guild_max_forum_categories}": "الحد الأقصى لتصنيفات المنتدى",
    "{guild_max_forum_threads}": "الحد الأقصى لثريد المنتدى",
    "{guild_max_forum_thread_members}": "الحد الأقصى لأعضاء ثريد المنتدى",
    "{guild_max_forum_forum_channels}": "الحد الأقصى لقنوات المنتدى للمنتدى",
    "{guild_max_forum_forum_tags}": "الحد الأقصى لعلامات المنتدى للمنتدى",
    "{guild_max_forum_forum_emojis}": "الحد الأقصى لإيموجيات المنتدى للمنتدى",
    "{guild_max_forum_forum_reactions}": "الحد الأقصى لتفاعلات المنتدى للمنتدى",
    "{guild_max_forum_forum_mentions}": "الحد الأقصى لمنشن المنتدى للمنتدى",
    "{guild_max_forum_forum_attachments}": "الحد الأقصى لمرفقات المنتدى للمنتدى",
    "{guild_max_forum_forum_webhooks}": "الحد الأقصى لويب هوك المنتدى للمنتدى",
    "{guild_max_forum_forum_invites}": "الحد الأقصى لدعوات المنتدى للمنتدى",
    "{guild_max_forum_forum_integrations}": "الحد الأقصى لتكاملات المنتدى للمنتدى",
    "{guild_max_forum_forum_emojis_per_message}": "الحد الأقصى لإيموجيات المنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_reactions_per_message}": "الحد الأقصى لتفاعلات المنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_mentions_per_message}": "الحد الأقصى لمنشن المنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_attachments_per_message}": "الحد الأقصى لمرفقات المنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_roles_per_channel}": "الحد الأقصى لرتب المنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_channels_per_category}": "الحد الأقصى لقنوات المنتدى للمنتدى لكل تصنيف",
    "{guild_max_forum_forum_categories}": "الحد الأقصى لتصنيفات المنتدى للمنتدى",
    "{guild_max_forum_forum_threads}": "الحد الأقصى لثريد المنتدى للمنتدى",
    "{guild_max_forum_forum_thread_members}": "الحد الأقصى لأعضاء ثريد المنتدى للمنتدى",
    "{guild_max_forum_forum_forum_channels}": "الحد الأقصى لقنوات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_tags}": "الحد الأقصى لعلامات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_emojis}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_reactions}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_mentions}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_attachments}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_webhooks}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_invites}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_integrations}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_emojis_per_message}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_reactions_per_message}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_mentions_per_message}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_attachments_per_message}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_roles_per_channel}": "الحد الأقصى لرتب المنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_channels_per_category}": "الحد الأقصى لقنوات المنتدى للمنتدى للمنتدى لكل تصنيف",
    "{guild_max_forum_forum_forum_categories}": "الحد الأقصى لتصنيفات المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_threads}": "الحد الأقصى لثريد المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_thread_members}": "الحد الأقصى لأعضاء ثريد المنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_channels}": "الحد الأقصى لقنوات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_tags}": "الحد الأقصى لعلامات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_emojis}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_reactions}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_mentions}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_attachments}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_webhooks}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_invites}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_integrations}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتدى",
    "{guild_max_forum_forum_forum_forum_emojis_per_message}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_forum_reactions_per_message}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_forum_mentions_per_message}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_forum_attachments_per_message}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتدى لكل رسالة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتدى لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتدى للمنتدى للمنتدى للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتدى للمنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتدى للمنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتدى للمنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� للمنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناة",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "الحد الأقصى لدعوات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_integrations_per_channel}": "الحد الأقصى لتكاملات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_emojis_per_channel}": "الحد الأقصى لإيموجيات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_reactions_per_channel}": "الحد الأقصى لتفاعلات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_mentions_per_channel}": "الحد الأقصى لمنشن المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_attachments_per_channel}": "الحد الأقصى لمرفقات المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_webhooks_per_channel}": "الحد الأقصى لويب هوك المنتد� لكل قناا",
    "{guild_max_forum_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت للسيرفر"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البUT لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسال دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_integrations_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_emojis_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_reactions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_mentions_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_attachments_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_webhooks_per_channel}": "✅ تم إرسل دعوة البوت لل Serrver"
    "{guild_max_forum_forum_invites_per_channel}": "✅ تم إرسل دعوة البوت <_SSO_TOKEN>