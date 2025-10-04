"""
React Native development profile for he2plus.

This profile sets up a complete React Native development environment
for cross-platform mobile app development.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class ReactNativeProfile(BaseProfile):
    """React Native development environment for cross-platform mobile apps."""

    def _initialize_profile(self) -> None:
        self.id = "mobile-react-native"
        self.name = "React Native Development"
        self.description = "Cross-platform mobile app development with React Native, TypeScript, and modern tooling"
        self.category = "mobile"
        self.version = "1.0.0"

        # Requirements
        self.requirements.ram_gb = 8.0
        self.requirements.disk_gb = 15.0
        self.requirements.cpu_cores = 4
        self.requirements.gpu_required = False
        self.requirements.internet_required = True
        self.requirements.download_size_mb = 2000.0
        self.requirements.supported_archs = ["x86_64", "arm64"]

        # Components
        self.components = [
            # Core runtime
            Component(
                id="language.node.18",
                name="Node.js 18 LTS",
                description="JavaScript runtime for React Native development",
                category="language",
                version="18",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["package_manager", "nvm", "volta", "official"]
            ),
            
            # Package managers
            Component(
                id="tool.npm",
                name="npm",
                description="Node Package Manager (comes with Node.js)",
                category="tool",
                download_size_mb=0.0,
                install_time_minutes=0,
                install_methods=["package_manager"]
            ),
            
            Component(
                id="tool.yarn",
                name="Yarn",
                description="Fast, reliable, and secure dependency management",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm", "package_manager"]
            ),
            
            # Version control
            Component(
                id="tool.git",
                name="Git",
                description="Version control system",
                category="tool",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["package_manager", "official"]
            ),
            
            # React Native CLI
            Component(
                id="tool.react-native-cli",
                name="React Native CLI",
                description="Command-line interface for React Native",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            # Expo CLI (alternative)
            Component(
                id="tool.expo-cli",
                name="Expo CLI",
                description="Command-line interface for Expo",
                category="tool",
                download_size_mb=15.0,
                install_time_minutes=3,
                install_methods=["npm"]
            ),
            
            # TypeScript support
            Component(
                id="language.typescript",
                name="TypeScript",
                description="Typed JavaScript at scale",
                category="language",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["npm", "package_manager"]
            ),
            
            # Android development
            Component(
                id="tool.android-studio",
                name="Android Studio",
                description="Official Android development environment",
                category="tool",
                download_size_mb=1000.0,
                install_time_minutes=30,
                install_methods=["official"]
            ),
            
            Component(
                id="tool.android-sdk",
                name="Android SDK",
                description="Android Software Development Kit",
                category="tool",
                download_size_mb=500.0,
                install_time_minutes=15,
                install_methods=["android-studio"]
            ),
            
            Component(
                id="tool.java",
                name="Java Development Kit",
                description="Java Development Kit for Android development",
                category="tool",
                download_size_mb=200.0,
                install_time_minutes=10,
                install_methods=["package_manager", "official"]
            ),
            
            # iOS development (macOS only)
            Component(
                id="tool.xcode",
                name="Xcode",
                description="Apple's development environment for iOS",
                category="tool",
                download_size_mb=15000.0,
                install_time_minutes=120,
                install_methods=["app-store"],
                supported_platforms=["macos"]
            ),
            
            Component(
                id="tool.ios-simulator",
                name="iOS Simulator",
                description="iOS device simulator (comes with Xcode)",
                category="tool",
                download_size_mb=0.0,
                install_time_minutes=0,
                install_methods=["xcode"],
                supported_platforms=["macos"]
            ),
            
            Component(
                id="tool.cocoapods",
                name="CocoaPods",
                description="Dependency manager for iOS projects",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=3,
                install_methods=["gem", "package_manager"],
                supported_platforms=["macos"]
            ),
            
            # Development tools
            Component(
                id="tool.vscode",
                name="Visual Studio Code",
                description="Code editor with excellent React Native support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            # React Native and React ecosystem
            Component(
                id="framework.react-native",
                name="React Native",
                description="Framework for building native apps with React",
                category="framework",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react",
                name="React",
                description="A JavaScript library for building user interfaces",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react-native-reanimated",
                name="React Native Reanimated",
                description="High-performance animations for React Native",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react-native-gesture-handler",
                name="React Native Gesture Handler",
                description="Native-driven gesture system for React Native",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Navigation
            Component(
                id="library.react-navigation",
                name="React Navigation",
                description="Routing and navigation for React Native apps",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # State management
            Component(
                id="library.redux-toolkit",
                name="Redux Toolkit",
                description="The official, opinionated, batteries-included toolset for efficient Redux development",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.zustand",
                name="Zustand",
                description="Small, fast and scalable state management solution",
                category="library",
                download_size_mb=0.5,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # UI components
            Component(
                id="library.react-native-elements",
                name="React Native Elements",
                description="Cross-platform React Native UI toolkit",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.native-base",
                name="NativeBase",
                description="Mobile-first component library for React Native",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.tamagui",
                name="Tamagui",
                description="Universal React design system",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Testing
            Component(
                id="tool.jest",
                name="Jest",
                description="JavaScript testing framework",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.detox",
                name="Detox",
                description="Gray box end-to-end testing for React Native",
                category="tool",
                download_size_mb=20.0,
                install_time_minutes=5,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.maestro",
                name="Maestro",
                description="Mobile UI automation testing framework",
                category="tool",
                download_size_mb=15.0,
                install_time_minutes=3,
                install_methods=["official"]
            ),
            
            # Code quality
            Component(
                id="tool.eslint",
                name="ESLint",
                description="JavaScript and TypeScript linter",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="tool.prettier",
                name="Prettier",
                description="Code formatter",
                category="tool",
                download_size_mb=2.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Debugging
            Component(
                id="tool.flipper",
                name="Flipper",
                description="Platform for debugging mobile apps",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["official"]
            ),
            
            Component(
                id="tool.react-native-debugger",
                name="React Native Debugger",
                description="Standalone app for debugging React Native apps",
                category="tool",
                download_size_mb=50.0,
                install_time_minutes=3,
                install_methods=["official"]
            ),
            
            # Performance monitoring
            Component(
                id="library.flipper-plugin-react-native-performance",
                name="Flipper React Native Performance",
                description="Performance monitoring plugin for Flipper",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Backend integration
            Component(
                id="library.apollo-client",
                name="Apollo Client",
                description="GraphQL client for React Native",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.axios",
                name="Axios",
                description="Promise-based HTTP client",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            # Storage
            Component(
                id="library.react-native-async-storage",
                name="React Native AsyncStorage",
                description="Asynchronous, persistent, key-value storage",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.realm",
                name="Realm",
                description="Mobile database for React Native",
                category="library",
                download_size_mb=5.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Push notifications
            Component(
                id="library.react-native-push-notification",
                name="React Native Push Notification",
                description="Push notification library for React Native",
                category="library",
                download_size_mb=2.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            # Camera and media
            Component(
                id="library.react-native-camera",
                name="React Native Camera",
                description="Camera component for React Native",
                category="library",
                download_size_mb=3.0,
                install_time_minutes=2,
                install_methods=["npm"]
            ),
            
            Component(
                id="library.react-native-image-picker",
                name="React Native Image Picker",
                description="Image picker for React Native",
                category="library",
                download_size_mb=1.0,
                install_time_minutes=1,
                install_methods=["npm"]
            ),
        ]

        # Verification steps
        self.verification_steps = [
            VerificationStep(
                name="Node.js Version",
                command="node --version",
                contains_text="v18"
            ),
            VerificationStep(
                name="npm Version",
                command="npm --version"
            ),
            VerificationStep(
                name="Git Version",
                command="git --version",
                contains_text="git version"
            ),
            VerificationStep(
                name="React Native CLI",
                command="npx react-native --version",
                contains_text="react-native"
            ),
            VerificationStep(
                name="TypeScript",
                command="npx tsc --version",
                contains_text="Version"
            ),
            VerificationStep(
                name="Android SDK",
                command="echo $ANDROID_HOME",
                contains_text="/"
            ),
            VerificationStep(
                name="Java Version",
                command="java -version",
                contains_text="version"
            ),
            VerificationStep(
                name="Jest",
                command="npx jest --version",
                contains_text="."
            ),
            VerificationStep(
                name="ESLint",
                command="npx eslint --version",
                contains_text="v"
            ),
            VerificationStep(
                name="Prettier",
                command="npx prettier --version",
                contains_text="."
            ),
        ]

        # Sample project
        self.sample_project = SampleProject(
            name="React Native Starter App",
            description="A complete React Native project with TypeScript, navigation, and modern tooling",
            type="create_app",
            source="npx react-native@latest init MyReactNativeApp --template react-native-template-typescript",
            directory="~/MyReactNativeApp",
            setup_commands=[
                "cd ~/MyReactNativeApp",
                "npm install",
                "npx react-native run-android  # For Android",
                "npx react-native run-ios      # For iOS (macOS only)"
            ],
            next_steps=[
                "Open Android Studio and start an emulator",
                "Run 'npx react-native run-android' for Android",
                "Run 'npx react-native run-ios' for iOS (macOS only)",
                "Start Metro bundler: npx react-native start",
                "Open the app on your device or emulator"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 React Native development environment ready!",
            "",
            "📚 Quick Start:",
            "  • Create new project: npx react-native@latest init MyApp --template react-native-template-typescript",
            "  • Start Metro bundler: npx react-native start",
            "  • Run on Android: npx react-native run-android",
            "  • Run on iOS: npx react-native run-ios (macOS only)",
            "",
            "🛠️  Development Tools:",
            "  • VS Code with React Native extensions",
            "  • Android Studio for Android development",
            "  • Xcode for iOS development (macOS only)",
            "  • Flipper for debugging",
            "  • React Native Debugger for advanced debugging",
            "",
            "📱 Platform Setup:",
            "  • Android: Install Android Studio and SDK",
            "  • iOS: Install Xcode and iOS Simulator (macOS only)",
            "  • Set up environment variables (ANDROID_HOME, etc.)",
            "  • Configure device/emulator for testing",
            "",
            "📦 Key Libraries:",
            "  • React Native 0.72+ with New Architecture",
            "  • TypeScript for type safety",
            "  • React Navigation for routing",
            "  • Redux Toolkit for state management",
            "  • React Native Reanimated for animations",
            "  • Jest for testing",
            "  • Detox for E2E testing",
            "",
            "🚀 Deployment Options:",
            "  • Google Play Store (Android)",
            "  • Apple App Store (iOS)",
            "  • Expo Application Services (EAS)",
            "  • CodePush for over-the-air updates",
            "  • Fastlane for automated deployment",
            "",
            "📖 Resources:",
            "  • React Native Documentation: https://reactnative.dev/docs",
            "  • React Navigation: https://reactnavigation.org",
            "  • TypeScript Handbook: https://www.typescriptlang.org/docs",
            "  • Android Development: https://developer.android.com",
            "  • iOS Development: https://developer.apple.com/ios",
            "",
            "💡 Pro Tips:",
            "  • Use TypeScript for better development experience",
            "  • Leverage New Architecture for better performance",
            "  • Implement proper error boundaries",
            "  • Use Flipper for debugging and performance monitoring",
            "  • Set up proper testing with Jest and Detox",
            "  • Use CodePush for quick updates without app store review",
            "",
            "🔗 Community:",
            "  • React Native Discord: https://discord.gg/reactnative",
            "  • React Native Community: https://github.com/react-native-community",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/react-native",
            "  • Reddit: https://reddit.com/r/reactnative",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/facebook/react-native/issues",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/react-native",
            "  • React Native Help: https://reactnative.dev/help"
        ]

    def get_installation_plan(self) -> Dict[str, any]:
        """Get detailed installation plan for this profile."""
        return {
            "profile": {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "category": self.category,
                "version": self.version
            },
            "requirements": {
                "ram_gb": self.requirements.ram_gb,
                "disk_gb": self.requirements.disk_gb,
                "cpu_cores": self.requirements.cpu_cores,
                "gpu_required": self.requirements.gpu_required,
                "internet_required": self.requirements.internet_required,
                "download_size_mb": self.requirements.download_size_mb,
                "supported_archs": self.requirements.supported_archs
            },
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "description": comp.description,
                    "category": comp.category,
                    "version": comp.version,
                    "download_size_mb": comp.download_size_mb,
                    "install_time_minutes": comp.install_time_minutes,
                    "install_methods": comp.install_methods,
                    "supported_platforms": getattr(comp, 'supported_platforms', ["macos", "linux", "windows"])
                }
                for comp in self.components
            ],
            "verification": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text,
                    "timeout_seconds": step.timeout_seconds
                }
                for step in self.verification_steps
            ],
            "sample_project": {
                "name": self.sample_project.name,
                "description": self.sample_project.description,
                "type": self.sample_project.type,
                "source": self.sample_project.source,
                "directory": self.sample_project.directory,
                "setup_commands": self.sample_project.setup_commands,
                "next_steps": self.sample_project.next_steps
            },
            "next_steps": self.next_steps,
            "estimated_total_time_minutes": sum(comp.install_time_minutes for comp in self.components),
            "estimated_download_size_mb": sum(comp.download_size_mb for comp in self.components),
            "mobile_specific": {
                "platforms": ["Android", "iOS"],
                "languages": ["JavaScript", "TypeScript", "Java", "Swift", "Kotlin"],
                "frameworks": ["React Native", "Expo"],
                "development_tools": ["Android Studio", "Xcode", "Flipper", "React Native Debugger"],
                "testing": ["Jest", "Detox", "Maestro", "React Native Testing Library"],
                "deployment": ["Google Play Store", "Apple App Store", "EAS", "CodePush"],
                "state_management": ["Redux Toolkit", "Zustand", "React Context", "MobX"],
                "navigation": ["React Navigation", "React Native Navigation"],
                "ui_libraries": ["React Native Elements", "NativeBase", "Tamagui", "UI Kitten"],
                "popular_libraries": [
                    "React Native Reanimated", "React Native Gesture Handler",
                    "React Native Vector Icons", "React Native AsyncStorage",
                    "React Native Image Picker", "React Native Camera"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for React Native projects."""
        return [
            "1. Create new React Native project: npx react-native@latest init MyApp --template react-native-template-typescript",
            "2. Navigate to project: cd MyApp",
            "3. Install dependencies: npm install",
            "4. Start Metro bundler: npx react-native start",
            "5. Open Android Studio and start an emulator",
            "6. Run on Android: npx react-native run-android",
            "7. Run on iOS: npx react-native run-ios (macOS only)",
            "8. Edit code in src/ directory",
            "9. Add components in components/ directory",
            "10. Configure navigation in navigation/ directory",
            "11. Write tests with Jest and React Native Testing Library",
            "12. Run tests: npm test",
            "13. Build for production: npx react-native run-android --variant=release",
            "14. Deploy to app stores using Fastlane",
            "15. Monitor with Flipper and performance tools"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common React Native issues."""
        return {
            "Installation Issues": [
                "Node.js version compatibility - ensure Node.js 18+ is installed",
                "Android SDK not found - set ANDROID_HOME environment variable",
                "Java version issues - ensure Java 11+ is installed",
                "Xcode not found - install Xcode from App Store (macOS only)",
                "CocoaPods issues - run 'pod install' in ios/ directory (macOS only)",
                "Permission errors - use 'sudo' on Linux/macOS or run as administrator on Windows"
            ],
            "Development Issues": [
                "Metro bundler not starting - clear cache with 'npx react-native start --reset-cache'",
                "Android emulator not starting - check AVD configuration in Android Studio",
                "iOS simulator not starting - check Xcode installation and iOS Simulator",
                "Hot reload not working - restart Metro bundler and reload app",
                "TypeScript errors - check tsconfig.json configuration",
                "Import errors - check import paths and file extensions"
            ],
            "Build Issues": [
                "Android build failures - check Android SDK and build tools version",
                "iOS build failures - check Xcode version and iOS deployment target",
                "Gradle build errors - clean and rebuild: cd android && ./gradlew clean",
                "CocoaPods errors - update pods: cd ios && pod install",
                "Memory issues - increase Node.js memory limit: NODE_OPTIONS='--max-old-space-size=4096'",
                "Network issues - check proxy settings and firewall configuration"
            ],
            "Performance Issues": [
                "Slow app performance - enable New Architecture and optimize components",
                "Large bundle size - use dynamic imports and code splitting",
                "Slow builds - enable parallel builds and increase memory",
                "Memory leaks - check for proper cleanup in useEffect hooks",
                "Slow navigation - optimize navigation structure and use lazy loading",
                "Slow animations - use React Native Reanimated for better performance"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for React Native development."""
        return [
            "ms-vscode.vscode-typescript-next",
            "ms-vscode.vscode-react-native",
            "ms-vscode.vscode-react-native-tools",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-eslint",
            "ms-vscode.vscode-json",
            "formulahendry.auto-rename-tag",
            "christian-kohler.path-intellisense",
            "ms-vscode.vscode-html-css-support",
            "ms-vscode.vscode-css-peek",
            "ms-vscode.vscode-emmet",
            "ms-vscode.vscode-git",
            "ms-vscode.vscode-git-graph",
            "ms-vscode.vscode-gitlens",
            "ms-vscode.vscode-thunder-client",
            "ms-vscode.vscode-restclient",
            "ms-vscode.vscode-jest",
            "ms-vscode.vscode-react-native-tools",
            "ms-vscode.vscode-react-native-tools",
            "ms-vscode.vscode-react-native-tools"
        ]

    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for React Native development."""
        return {
            "React Native Commands": [
                "npx react-native@latest init MyApp --template react-native-template-typescript",
                "npx react-native start - Start Metro bundler",
                "npx react-native run-android - Run on Android",
                "npx react-native run-ios - Run on iOS (macOS only)",
                "npx react-native run-android --variant=release - Build for production",
                "npx react-native run-ios --configuration Release - Build for production",
                "npx react-native --version - Check React Native version"
            ],
            "Package Management": [
                "npm install - Install dependencies",
                "npm install package-name - Install package",
                "npm install -D package-name - Install dev dependency",
                "npm uninstall package-name - Remove package",
                "npm update - Update all packages",
                "npm audit - Check for vulnerabilities",
                "npm audit fix - Fix vulnerabilities"
            ],
            "Android Commands": [
                "cd android && ./gradlew clean - Clean Android build",
                "cd android && ./gradlew assembleDebug - Build debug APK",
                "cd android && ./gradlew assembleRelease - Build release APK",
                "adb devices - List connected devices",
                "adb install app.apk - Install APK on device",
                "adb logcat - View device logs"
            ],
            "iOS Commands": [
                "cd ios && pod install - Install CocoaPods dependencies",
                "cd ios && pod update - Update CocoaPods dependencies",
                "cd ios && xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 14' build - Build for iOS",
                "xcrun simctl list devices - List iOS simulators",
                "xcrun simctl boot 'iPhone 14' - Boot iOS simulator"
            ],
            "Development Tools": [
                "npx tsc --noEmit - Check TypeScript without emitting",
                "npx eslint . --ext .ts,.tsx - Lint TypeScript files",
                "npx prettier --write . - Format all files",
                "npx jest --watch - Run tests in watch mode",
                "npx react-native start --reset-cache - Start Metro with cache reset",
                "npx react-native doctor - Check development environment"
            ],
            "Debugging Commands": [
                "npx react-native log-android - View Android logs",
                "npx react-native log-ios - View iOS logs",
                "npx react-native start --verbose - Start Metro with verbose logging",
                "adb logcat | grep ReactNative - Filter Android logs for React Native",
                "xcrun simctl spawn booted log stream --predicate 'process == \"MyApp\"' - Filter iOS logs for app"
            ]
        }
