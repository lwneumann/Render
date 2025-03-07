import FileAnimate
import argparse
import importlib.util
import os
import sys

import FileAnimate.file_maker

def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    else:
        raise ImportError(f"Could not load module from {module_path}")

def main():
    parser = argparse.ArgumentParser(description="Renders given [simulation].py's `get_step()` function into the selected rendering mode")
    parser.add_argument("simulation", help="Python file to load simulaion from")
    parser.add_argument("-fps", type=int, default=30, help="Frames per second (30)")
    parser.add_argument("-seconds", type=int, default=5, help="Duration in seconds (5)")
    parser.add_argument("-length", type=int, default=100, help="Default length (100)")
    parser.add_argument("-height", type=int, default=100, help="Default height (100)")
    parser.add_argument("-width", type=int, default=0, help="Default width (100)")
    parser.add_argument("-mode", type=str, default="FileAnimate", help="Render Mode (png, mp4, Minecraft)")

    args = parser.parse_args()
    
    module = load_module(args.simulation)
    
    if hasattr(module, "get_step") and callable(module.get_step):
        size = [args.length, args.height]
        if args.width != 0:
            size.append(args.width)
        frames = args.fps * args.seconds
        sim_source = f"Simulation From: {args.simulation}"

        print()
        print(f"{'Settings':-^{len(sim_source)}}")
        print(f"FPS: {args.fps}")
        print(f"Seconds: {args.seconds}")
        print(f"Total Frames: {frames}")
        print(f"Mode: {args.mode}")
        print(f"Screen Size: {size}")
        print(sim_source)
        print()
        step_f = module.get_step(size)
        
        if args.mode == "FileAnimate":
            FileAnimate.file_maker.render_video(step_f, frames=frames, fps=args.fps)

    else:
        print(f"Error: {args.simulation} does not have a callable get_step() function.")

if __name__ == "__main__":
    main()
