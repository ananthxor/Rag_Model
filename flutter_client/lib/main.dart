import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:rag_client/ui/home_screen.dart';

void main() {
  runApp(const RagApp());
}

class RagApp extends StatelessWidget {
  const RagApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Local RAG',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF3B82F6),
          brightness: Brightness.dark,
          surface: const Color(0xFF0F172A),
          background: const Color(0xFF020617),
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
