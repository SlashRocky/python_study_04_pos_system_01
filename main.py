import csv
import os
import datetime


class RegisterProducts(object):
    def __init__(self):
        self.check_csv_file = os.path.exists('product_master.csv')
        self.fieldnames = ['CODE', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL']

    def display_product_list(self):
        if self.check_csv_file:
            print('\n現在登録されている商品は以下の通りです。\n')
            with open('product_master.csv', 'r') as rewrite_csv:
                existing_products = csv.DictReader(rewrite_csv)

                self.existing_product_list = []
                print(*self.fieldnames)
                for existing_product in existing_products:
                    print(
                        existing_product['CODE'],
                        existing_product['NAME'],
                        existing_product['PRICE'],
                        existing_product['QUANTITY'],
                        existing_product['TOTAL'],
                    )

        else:
            print('\n商品マスタCSVがありません。')

    def ask_of_registering_products(self):
        while True:
            self.answer_of_register_producs = input('\n商品登録をしますか？ Yes or No で答えてね！\n\n')
            if 'y' in self.answer_of_register_producs.lower():
                return True
            elif 'n' in self.answer_of_register_producs.lower():
                print('\nそれでは商品登録システムを終了します。')
                return False
            else:
                print('\nYesかNoで答えて下さいね！')

    def register_products(self):
        print('\nでは、商品を登録してみましょう！')
        while True:
            self.code = input('\nまず、登録したい商品の商品コードを入力してね！\n\n')
            self.name = input('\n次に、その商品の商品名を入力してね！\n\n')
            self.price = input('\n次に、その商品の価格を入力してね！\n\n')
            self.quantity = input('\n最後に、その商品の個数を入力してね！\n\n')
            self.total = int(self.price) * int(self.quantity)

            with open('product_master.csv', 'a') as add_to_csv:
                writer = csv.DictWriter(add_to_csv, fieldnames=self.fieldnames)
                writer.writerow({
                    'CODE': self.code,
                    'NAME': self.name,
                    'PRICE': self.price,
                    'QUANTITY': self.quantity,
                    'TOTAL': self.total,
                })

            self.other_products_registered = input('\n登録しました！\n他の商品も登録しますか？\nYes or No で答えてね！\n\n')

            if 'y' in self.other_products_registered:
                print('\nそれでは商品の登録を続けましょう！')
            else:
                print('\nそれではこれにて商品登録を終了します。')
                self.display_product_list()
                break

    def output_register_products(self):
        csv_file = open('product_master.csv', 'r')

        record_list = []
        record = csv_file.readline()
        while record:
            record_list.append(record.rstrip().split(','))
            record = csv_file.readline()

        now = datetime.datetime.now()
        output_master_time = now.strftime('%Y_%m%d_%H%M')

        with open(f'./product_master_txt/product_master_{output_master_time}.txt', 'w') as f:
            for record in record_list:
                f.write('\t'.join(record))
                f.write('\n')

    def __del__(self):
        pass


class PurchaseProducts(object):
    def __init__(self):
        pass

    def ask_of_purchase(self):
        while True:
            self.answer_of_purchase = input('\n商品を購入しますか？ Yes or No で答えてね！\n\n')
            if 'y' in self.answer_of_purchase.lower():
                return True
            elif 'n' in self.answer_of_purchase.lower():
                print('\n承知致しました。')
                return False
            else:
                print('\nYesかNoで答えて下さいね！')

    def check_inventory(self):
        while True:
            self.code_of_purchase = input('\n購入したい商品の商品コードを入力して下さい。\n\n')
            with open('product_master.csv', 'r') as check_quantity_csv:
                existing_products = csv.DictReader(check_quantity_csv)
                items = []
                for index, existing_product in enumerate(existing_products):
                    items.append(existing_product)
                    if items[index]['CODE'] == self.code_of_purchase:
                        self.target_product_quantity = int(items[index]['QUANTITY'])
                        self.target_product_price = int(items[index]['PRICE'])
                        self.target_product_name = items[index]['NAME']
            if self.target_product_quantity == 0:
                print('\n残念ですが、この商品は在庫切れでございます。\n')
                self.answer_continue_shopping = input('\n買い物を続けますか？\nYesかNoで答えて下さい！\n\n')
                if 'y' in self.answer_continue_shopping:
                    pass
                else:
                    return False
            else:
                return 'shopping_continue'

    def bill(self):
        while True:
            self.quantity_of_purchase = input('\nこの商品をいくつ購入しますか？\n数字を入力して下さい。\n\n')
            self.quantity_of_purchase = int(self.quantity_of_purchase)
            if self.quantity_of_purchase > self.target_product_quantity:
                print(f'\nこの商品は現在{self.target_product_quantity}個しかありません。\n{self.target_product_quantity}個以内のご購入でお願いします。')
            else:
                self.total_of_purchase = self.target_product_price * self.quantity_of_purchase
                print(f'\nひとつ{self.target_product_price}円のものが、{self.quantity_of_purchase}個ですので、合計{self.total_of_purchase}円になります。')
                break
        while True:
            self.payment_amount = input('\nお支払い金額の入力をお願いします。\n\n')
            self.payment_amount = int(self.payment_amount)
            if self.payment_amount < self.total_of_purchase:
                print('\n金額が不足しております。')
            elif self.payment_amount == self.total_of_purchase:
                print('\nちょうどのお支払い有難うございます！')
                break
            else:
                self.payment_change = self.payment_amount - self.total_of_purchase
                print(f'\n{self.payment_amount}円のお預かりですので、お釣りが{self.payment_change}円になります！')
                break

    def output_receipt(self):
        now = datetime.datetime.now()
        output_receipt_time = now.strftime('%Y_%m%d_%H%M')
        time_for_receipt = now.strftime('%Y年%m月%d日 %H時%M分')
        receipt_contents = time_for_receipt + '\n\n' \
                           + '領収書' + '\n' \
                           + self.target_product_name + '\n' \
                           + '@¥' + str(self.target_product_price) + ' × ' + str(self.quantity_of_purchase) + '個' + '\n' \
                           + '合計：¥' + str(self.total_of_purchase) + '\n' \
                           + 'お預かり：' + str(self.payment_amount) + '\n' \
                           + 'お釣り：' + str(self.payment_change) + '\n'

        with open(f'./receipt/receipt_{output_receipt_time}.txt', 'w') as f:
            f.write(receipt_contents)

    def pass_code_of_purchase(self):
        return self.code_of_purchase

    def pass_quantity_of_purchase(self):
        return self.quantity_of_purchase

    def __del__(self):
        print('\nまたのご来店をお待ちしております！')


class UpdateProductsData(object):
    def __init__(self, code_of_purchase, quantity_of_purchase):
        self.code_of_purchase = code_of_purchase
        self.quantity_of_purchase = quantity_of_purchase

    def update_products_master(self):
        with open('product_master.csv', 'r', encoding='UTF-8') as rf:
            reader = csv.reader(rf)
            # ヘッダー行を飛ばす
            next(reader)

            with open("product_master.csv", 'w', encoding='UTF-8') as wf:
                writer = csv.writer(wf)
                writer.writerow(['CODE', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL'])
                # 購入された分だけ在庫数を減らす
                for index, line in enumerate(reader):
                    if line[0] == self.code_of_purchase:
                        line[3] = int(line[3]) - self.quantity_of_purchase
                        line[4] = int(line[2]) * int(line[3])
                        writer.writerow([line[0], line[1], line[2], line[3], line[4]])
                    else:
                        writer.writerow([line[0], line[1], line[2], line[3], line[4]])

    def __del__(self):
        pass


if __name__ == '__main__':
    register_products = RegisterProducts()
    register_products.display_product_list()
    if register_products.ask_of_registering_products():
        register_products.register_products()
    register_products.output_register_products()
    del register_products
    purchase_products = PurchaseProducts()
    if purchase_products.ask_of_purchase():
        if purchase_products.check_inventory() == 'shopping_continue':
            purchase_products.bill()
            purchase_products.output_receipt()
            code_of_purchase = purchase_products.pass_code_of_purchase()
            quantity_of_purchase = purchase_products.pass_quantity_of_purchase()
            del purchase_products
            update_products_data = UpdateProductsData(code_of_purchase, quantity_of_purchase)
            update_products_data.update_products_master()
            del update_products_data
        else:
            pass
