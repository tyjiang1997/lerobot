import sys
import os

# 1. 确保能找到源码路径（如果没执行 pip install -e .）
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from lerobot.motors.feetech import FeetechMotorsBus
except ImportError as e:
    print(f"导入失败，请检查路径。错误信息: {e}")
    sys.exit(1)

def scan():
    port = "/dev/tty.usbmodem5AB01582561"  # 你的 Mac 端口
    
    # 初始化一个空的配置，不预设任何电机，这样就不会触发 "Missing motor" 错误
    bus = FeetechMotorsBus(port=port, motors={})
    # bus.connect()
    # bus.connect()
    bus.serial = bus._open_generate_serial()
    bus.is_connected = True
    print(f"✅ 已连接端口: {port}")
    print("开始扫描 ID 1-15 的电机 (请确保已接通 12V 电源)...")
    
    found_any = False
    # 直接调用底层的 read_with_id 方法来扫描
    for motor_id in range(1, 16):
        try:
            # 尝试读取电机的模型版本（寄存器 3 & 4）
            model = bus.read_with_id(motor_id, "Model", 2)
            if model:
                print(f"📍 发现电机！ID: {motor_id}")
                found_any = True
        except Exception:
            continue
            
    if not found_any:
        print("❌ 扫描完成，未发现任何电机。请检查 12V 电源和排线。")
            

if __name__ == "__main__":
    scan()