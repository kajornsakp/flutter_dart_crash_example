import '../models/index.dart';
import '../repository/index.dart';
import 'dart:math';

class ExampleModuleService implements ExampleModuleRepository {
  static const magicNumber = 5;
  static const int MAXN = 10000000;

  int generateRandomNumber() {
    var rng = Random();
    return (rng.nextInt(MAXN) + magicNumber) % MAXN;
  }

  @override
  ExampleModuleModel generateRandomModel() {
    int randomNumber = generateRandomNumber();
    ExampleModuleModel model = ExampleModuleModel.fromMap({"s": "", "n": randomNumber});
    return model;
  }
}