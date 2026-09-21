"""CLI entry point for rednote-cli.

Usage:
    rednote login / status / logout
    rednote search <keyword> [--sort popular|latest] [--type video|image] [--page N]
    rednote read <id_or_url> [--xsec-token TOKEN]
    rednote comments <id_or_url>
    rednote user <user_id>
    rednote user-posts <user_id> [--cursor CURSOR]
    rednote feed
    rednote hot [--category CATEGORY]
    rednote topics <keyword>
    rednote like <id_or_url> [--undo]
    rednote favorite <id_or_url>
    rednote unfavorite <id_or_url>
    rednote comment <id_or_url> --content "..."
    rednote reply <id_or_url> --comment-id ID --content "..."
    rednote favorites [user_id]
    rednote my-notes [--page N]
    rednote notifications [--type mentions|likes|connections]
    rednote unread
    rednote post --title "..." --body "..." --images img.png
    rednote delete <id_or_url> [-y]
"""

from __future__ import annotations

import logging
import sys

import click

from . import __version__
from .commands import auth, creator, interactions, notifications, reading, social
from .constants import COOKIE_DOMAINS, DEFAULT_COOKIE_DOMAIN


def _fix_windows_encoding() -> None:
    """Force UTF-8 on Windows where the default codepage (936/GBK) garbles output."""
    if sys.platform != "win32":
        return
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


_fix_windows_encoding()


@click.group()
@click.version_option(version=__version__, prog_name="rednote")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
@click.option(
    "--cookie-source",
    type=str,
    default="auto",
    show_default=True,
    help="Browser to read cookies from (auto = try all installed browsers)",
)
@click.option(
    "--cookie-domain",
    type=click.Choice(tuple(COOKIE_DOMAINS)),
    default=DEFAULT_COOKIE_DOMAIN,
    show_default=True,
    help="Website domain to read browser cookies from",
)
@click.pass_context
def cli(ctx, verbose: bool, cookie_source: str, cookie_domain: str):
    """rednote - Xiaohongshu CLI using RedNote browser cookies."""
    ctx.ensure_object(dict)
    ctx.obj["cookie_source"] = cookie_source
    ctx.obj["cookie_domain"] = cookie_domain

    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)


# ─── Auth commands ───────────────────────────────────────────────────────────

cli.add_command(auth.login)
cli.add_command(auth.status)
cli.add_command(auth.logout)
cli.add_command(auth.whoami)

# ─── Reading commands ────────────────────────────────────────────────────────

cli.add_command(reading.search)
cli.add_command(reading.read)
cli.add_command(reading.comments)
cli.add_command(reading.sub_comments)
cli.add_command(reading.user)
cli.add_command(reading.user_posts)
cli.add_command(reading.feed)
cli.add_command(reading.hot)
cli.add_command(reading.topics)
cli.add_command(reading.search_user)

# ─── Interaction commands ────────────────────────────────────────────────────

cli.add_command(interactions.like)
cli.add_command(interactions.favorite)
cli.add_command(interactions.unfavorite)
cli.add_command(interactions.comment)
cli.add_command(interactions.reply)
cli.add_command(interactions.delete_comment)

# ─── Social commands ────────────────────────────────────────────────────────

cli.add_command(social.follow)
cli.add_command(social.unfollow)
cli.add_command(social.favorites)
cli.add_command(social.likes)

# ─── Creator commands ───────────────────────────────────────────────────────

cli.add_command(creator.post)
cli.add_command(creator.my_notes)
cli.add_command(creator.delete)

# ─── Notification commands ──────────────────────────────────────────────────

cli.add_command(notifications.notifications)
cli.add_command(notifications.unread)

if __name__ == "__main__":
    cli()
