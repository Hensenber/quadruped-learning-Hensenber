#include <iomanip>
#include <iostream>
class Motor {
public:
virtual void enable() = 0;
virtual void setPosition(double position) = 0;
virtual double getPosition() const = 0;
virtual ~Motor() = default;
};
class DMMotor : public Motor {
public:
explicit DMMotor(int id) : id_(id) {}