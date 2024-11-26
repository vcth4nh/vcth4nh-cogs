from redbot.core import VersionInfo, version_info
from redbot.core.utils import get_end_user_data_statement
from .ctfreg import CtfReg

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


async def setup(bot):
    await bot.add_cog(CtfReg(bot))
