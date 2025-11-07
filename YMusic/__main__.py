import importlib
import asyncio
import sys
from pytgcalls import idle

from YMusic import LOGGER
from YMusic.plugins import ALL_MODULES
from YMusic import app, call

async def init():
    try:
        # بدء التطبيق
        await app.start()
        LOGGER("YMusic").info("Account Started Successfully")

        # استيراد جميع الموديولات
        for all_module in ALL_MODULES:
            importlib.import_module("YMusic.plugins" + all_module)

        LOGGER("YMusic.plugins").info("Successfully Imported Modules")
        
        # بدء المكالمات
        await call.start()
        await idle()
        
    except Exception as e:
        LOGGER("YMusic").error(f"Error: {e}")
        raise

def main():
    try:
        # إنشاء حلقة أحداث جديدة
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # تشغيل الكود
        loop.run_until_complete(init())
        
    except KeyboardInterrupt:
        LOGGER("YMusic").info("Received interrupt signal")
    except Exception as e:
        LOGGER("YMusic").error(f"Fatal error: {e}")
    finally:
        LOGGER("YMusic").info("Stopping YMusic Bot! GoodBye")
        # تنظيف الموارد
        try:
            loop.run_until_complete(app.stop())
            loop.run_until_complete(call.stop())
        except:
            pass
        loop.close()

if __name__ == "__main__":
    main()
