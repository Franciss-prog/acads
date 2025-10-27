class InkPrinter:
    def print_document(self):

        print("Sprays liquid ink droplets through tiny nozzles.")


class LaserPrinter:
    def print_document(self):
        print(
            "Uses a laser to charge a drum, which attracts powdered toner to the paper, and then uses heat to fuse it."
        )


# Test
printers = [InkPrinter(), LaserPrinter()]
for printer in printers:
    printer.print_document()
