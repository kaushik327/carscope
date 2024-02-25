import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/',
      routes: {
        '/': (context) => HomePage(),
        '/second': (context) => ImagePage(),
      },
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Background Image
              const Image(
                image: NetworkImage('https://scontent-ord5-1.xx.fbcdn.net/v/t1.15752-9/429600448_256598337490606_2217278646480399904_n.png?_nc_cat=106&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=7rYUvId8dIcAX-i15Up&_nc_ht=scontent-ord5-1.xx&oh=03_AdSWCycfENwVPaECIGKgou4CF40Zfc4pPRKEJ1uK6cVRSQ&oe=66010E47'), // Replace with your image URL
                height: 384
              ),
              // Content
              Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    const Text(
                      'Welcome to CarScope!',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.red,
                      ),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pushNamed(context, '/second');
                      },
                      child: const Text('Start'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ImagePage extends StatefulWidget {
  const ImagePage({super.key});

  @override
  State<ImagePage> createState() => _ImagePageState();
}
class _ImagePageState extends State<ImagePage> {

  var uuid = const Uuid();
  var _image;
  final ImagePicker picker = ImagePicker();
  late String summary;
  bool button_pressed = false;

  Future imageFromGallery() async {
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);
    setState(() {
      _image = File(image!.path);
    });
  }

  Future imageFromCamera() async {
    final XFile? image = await picker.pickImage(source: ImageSource.camera);
    setState(() {
      _image = File(image!.path);
    });
  }

  Future classify() async {

    var request = http.MultipartRequest('POST', Uri.parse('http://127.0.0.1:5000/upload_image'));
    request.files.add(
      http.MultipartFile(
        'file',
        _image.readAsBytes().asStream(),
        _image.lengthSync(), 
        filename: '${uuid.v4()}.png'
      )
    );
    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode != 200) {
      return "what";
    }
    setState(() {
      summary = jsonDecode(response.body)['response'];
      button_pressed = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Take a picture!'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextButton(
              onPressed: imageFromCamera,
              child: const Text("From camera"),
            ),
            TextButton(
              onPressed: imageFromGallery,
              child: const Text("From gallery"),
            ),
            FilledButton(
              onPressed: classify,
              child: const Text("Classify")
            ),
            button_pressed 
              ? Text(summary)
              : const SizedBox.shrink()
          ]
        )
      )
    );
  }

}