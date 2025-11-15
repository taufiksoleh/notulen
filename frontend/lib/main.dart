import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'screens/home_screen.dart';
import 'screens/meeting_detail_screen.dart';
import 'screens/record_screen.dart';

void main() {
  runApp(const ProviderScope(child: NotulenApp()));
}

class NotulenApp extends StatelessWidget {
  const NotulenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Notulen',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
        cardTheme: CardTheme(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          filled: true,
        ),
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
        cardTheme: CardTheme(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          filled: true,
        ),
      ),
      themeMode: ThemeMode.system,
      home: const HomeScreen(),
      routes: {
        '/home': (context) => const HomeScreen(),
        '/record': (context) => const RecordScreen(),
      },
      onGenerateRoute: (settings) {
        if (settings.name?.startsWith('/meeting/') ?? false) {
          final meetingId = int.tryParse(settings.name!.split('/').last);
          if (meetingId != null) {
            return MaterialPageRoute(
              builder: (context) => MeetingDetailScreen(meetingId: meetingId),
            );
          }
        }
        return null;
      },
    );
  }
}
