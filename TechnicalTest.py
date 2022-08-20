
#!/usr/bin/env python3
if __name__ == "__main__":
    import re
    from ReciptReader import ReciptReader

    OCR1 = ReciptReader('OCR1.txt')
    print(OCR1.getComponets())

    OCR2 = ReciptReader('OCR2.txt')
    print(OCR2.getComponets())