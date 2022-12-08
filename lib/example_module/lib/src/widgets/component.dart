import '../domain/index.dart';
// [Replace] widget_deps
import 'package:flutter/material.dart';

class ExampleModuleComponent extends StatelessWidget {
  const ExampleModuleComponent({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    ExampleModuleRepository repo = ExampleModuleService();
    var model = repo.generateRandomModel();
    return Column(
      children: [
        Text("Random number is ${model.n}"),
// [Replace] children
      ],
    );
  }
}