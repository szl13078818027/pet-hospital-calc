from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# ========== 主题色 ==========
C_BG = '#EAF2F0'
C_CARD = '#FFFFFF'
C_PRIMARY = '#2A9D8F'
C_PRIMARY_DK = '#1F7A6E'
C_SECONDARY = '#D7ECE8'
C_TEXT = '#1F3A36'
C_MUTED = '#5B7C78'
C_WARN = '#C7532C'

Window.size = (380, 760)
Window.clearcolor = get_color_from_hex(C_BG)


def to_float(text, default=0.0):
    """把输入框文本安全地转成 float；空或非法时回退默认值。"""
    try:
        if text is None or text.strip() == "":
            return default
        return float(text)
    except (ValueError, TypeError):
        return default


# ========== 美化控件 ==========
class RoundedButton(Button):
    def __init__(self, bg_color=C_PRIMARY, text_color='#FFFFFF', **kwargs):
        super().__init__(**kwargs)
        self._bg = get_color_from_hex(bg_color)
        self.color = get_color_from_hex(text_color)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bold = True
        self.font_size = dp(16)
        with self.canvas.before:
            self._col = Color(rgba=self._bg)
            self._rr = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *a):
        self._rr.pos = self.pos
        self._rr.size = self.size


class FieldInput(TextInput):
    def __init__(self, **kwargs):
        kwargs.setdefault('foreground_color', get_color_from_hex(C_TEXT))
        kwargs.setdefault('cursor_color', get_color_from_hex(C_PRIMARY))
        kwargs.setdefault('font_size', dp(15))
        kwargs.setdefault('multiline', False)
        kwargs.setdefault('padding', [dp(10), dp(10), dp(10), dp(10)])
        kwargs['background_color'] = (0, 0, 0, 0)
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex(C_CARD))
            self._rr = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *a):
        self._rr.pos = self.pos
        self._rr.size = self.size


class FieldLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', get_color_from_hex(C_MUTED))
        kwargs.setdefault('font_size', dp(12.5))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(18))
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)
        self.bind(width=lambda inst, w: inst.setter('text_size')(inst, (w, None)))


class HeaderLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', get_color_from_hex(C_TEXT))
        kwargs.setdefault('font_size', dp(20))
        kwargs.setdefault('bold', True)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(34))
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)
        self.bind(width=lambda inst, w: inst.setter('text_size')(inst, (w, None)))


class ResultLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', get_color_from_hex(C_TEXT))
        kwargs.setdefault('font_size', dp(13.5))
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'top')
        kwargs.setdefault('padding', (dp(12), dp(12)))
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex(C_CARD))
            self._rr = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._upd, size=self._upd)
        self.bind(width=lambda inst, w: inst.setter('text_size')(inst, (w - dp(24), None)))

    def _upd(self, *a):
        self._rr.pos = self.pos
        self._rr.size = self.size


# ========== 页面1：门店盈亏测算 ==========
class ScreenProfit(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(14))

        root.add_widget(HeaderLabel(text='门店盈亏测算'))

        root.add_widget(FieldLabel(text='一次性前期总投入(元)'))
        self.input_invest = FieldInput(hint_text='例:1200000', input_filter='float')
        root.add_widget(self.input_invest)

        root.add_widget(FieldLabel(text='每月租金(元)'))
        self.input_rent = FieldInput(hint_text='例:8000', input_filter='float')
        root.add_widget(self.input_rent)

        root.add_widget(FieldLabel(text='每月人工总工资(元)'))
        self.input_salary = FieldInput(hint_text='例:25000', input_filter='float')
        root.add_widget(self.input_salary)

        root.add_widget(FieldLabel(text='其他每月固定开支(水电/折旧/宽带)(元)'))
        self.input_fix_other = FieldInput(hint_text='例:3000', input_filter='float')
        root.add_widget(self.input_fix_other)

        root.add_widget(FieldLabel(text='预估月总营收(元)'))
        self.input_revenue = FieldInput(hint_text='例:60000', input_filter='float')
        root.add_widget(self.input_revenue)

        root.add_widget(FieldLabel(text='变动成本率(耗材药品，填百分比，如25代表25%)'))
        self.input_var_rate = FieldInput(hint_text='例:25', input_filter='float')
        root.add_widget(self.input_var_rate)

        btn_calc = RoundedButton(text='测算盈亏')
        btn_calc.bind(on_press=self.calc_profit)
        root.add_widget(btn_calc)

        btn_switch = RoundedButton(
            text='切换到【股权测算】',
            bg_color=C_SECONDARY, text_color=C_PRIMARY_DK,
            size_hint_y=0.7,
        )
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'screen_stock'))
        root.add_widget(btn_switch)

        self.result_label = ResultLabel(size_hint_y=1)
        root.add_widget(self.result_label)
        self.add_widget(root)

    def calc_profit(self, instance):
        try:
            invest = to_float(self.input_invest.text)
            rent = to_float(self.input_rent.text)
            salary = to_float(self.input_salary.text)
            fix_other = to_float(self.input_fix_other.text)
            revenue = to_float(self.input_revenue.text)
            var_rate = to_float(self.input_var_rate.text) / 100.0

            if var_rate >= 1.0:
                self.result_label.text = '变动成本率需小于100%，请重新填写。'
                return

            fixed_total = rent + salary + fix_other
            margin_contribution = revenue * (1 - var_rate)
            monthly_profit = margin_contribution - fixed_total
            break_even = fixed_total / (1 - var_rate) if (1 - var_rate) > 0 else 99999999
            annual_profit = monthly_profit * 12

            if monthly_profit > 0 and invest > 0:
                payback = invest / monthly_profit
                pay_text = f'{payback:.1f} 个月'
                roi = annual_profit / invest * 100
                roi_text = f'{roi:.1f} %'
            else:
                pay_text = '无法回本(当前亏损)'
                roi_text = '— (未盈利/总投入为0)'

            txt = (
                '==== 经营盈亏测算 ====\n'
                f'每月固定总成本：{fixed_total:,.0f} 元\n'
                f'保本月营业额：{break_even:,.0f} 元\n'
                f'月度预估净利润：{monthly_profit:,.0f} 元\n'
                f'年度预估净利润：{annual_profit:,.0f} 元\n'
                f'年化回报率 ROI：{roi_text}\n'
                '正数盈利｜负数亏损\n'
                f'预计回本周期：{pay_text}'
            )
            self.result_label.text = txt
        except Exception as e:
            self.result_label.text = f'输入错误！\n{e}'


# ========== 页面2：股权测算 【资金股70%｜技术干股30%】 ==========
class ScreenStock(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(14))

        root.add_widget(HeaderLabel(text='股权架构测算'))

        root.add_widget(FieldLabel(text='项目总资金出资额（资金股东合计）'))
        self.input_total_fund = FieldInput(hint_text='例:1200000', input_filter='float')
        root.add_widget(self.input_total_fund)

        root.add_widget(FieldLabel(text='资金股东人数'))
        self.input_fund_shareholder_cnt = FieldInput(hint_text='例:40', input_filter='float')
        root.add_widget(self.input_fund_shareholder_cnt)

        root.add_widget(FieldLabel(text='单资金股东个人出资额'))
        self.input_person_fund = FieldInput(hint_text='例:10000', input_filter='float')
        root.add_widget(self.input_person_fund)

        root.add_widget(FieldLabel(text='在职医生人数（分摊30%技术股）'))
        self.input_doctor_cnt = FieldInput(hint_text='例:3', input_filter='float')
        root.add_widget(self.input_doctor_cnt)

        btn_calc = RoundedButton(text='计算股权')
        btn_calc.bind(on_press=self.calc_stock)
        root.add_widget(btn_calc)

        btn_switch = RoundedButton(
            text='切换到【盈亏测算】',
            bg_color=C_SECONDARY, text_color=C_PRIMARY_DK,
            size_hint_y=0.7,
        )
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'screen_profit'))
        root.add_widget(btn_switch)

        self.result_label = ResultLabel(size_hint_y=1)
        root.add_widget(self.result_label)
        self.add_widget(root)

    def calc_stock(self, instance):
        try:
            total_fund = to_float(self.input_total_fund.text)
            fund_share_cnt = to_float(self.input_fund_shareholder_cnt.text)
            person_fund = to_float(self.input_person_fund.text)
            doctor_cnt = to_float(self.input_doctor_cnt.text)

            if total_fund <= 0:
                self.result_label.text = '请填写有效的【项目总资金出资额】(大于0)。'
                return
            if doctor_cnt <= 0:
                self.result_label.text = '请填写有效的【在职医生人数】(大于0)。'
                return

            fund_ratio = 0.70  # 资金股固定70%
            tech_ratio = 0.30  # 技术干股固定30%
            project_valuation = total_fund / fund_ratio

            # 单个资金股东占项目总股权
            person_total_share = (person_fund / total_fund) * fund_ratio
            # 单个医生分得技术股
            single_doctor_share = tech_ratio / doctor_cnt

            hint = ''
            if fund_share_cnt > 0:
                avg = total_fund / fund_share_cnt
                hint = f'\n资金股东人均出资：{avg:,.0f} 元\n'
                if abs(person_fund * fund_share_cnt - total_fund) / total_fund > 0.05:
                    hint += '⚠️ 个人出资×人数 与 总出资额 偏差>5%，请核对。\n'

            txt = (
                '==== 股权测算【资金股70%｜技术股30%】====\n'
                f'项目整体估值：{project_valuation:,.0f} 元\n'
                '（估值 = 出资金额 ÷ 资金股占比70%）\n'
                '资金股东合计占股：70.00%\n'
                '在职医生技术干股合计：30.00%\n\n'
                f'单个资金股东（出资{person_fund:,.0f}元）\n'
                f'=> 占项目总股权：{person_total_share*100:.2f} %\n\n'
                f'{doctor_cnt:.0f}名在职医生平分30%技术股\n'
                f'每名医生在职股：{single_doctor_share*100:.2f}%\n'
                f'{hint}\n'
                '⚠️规则说明：\n'
                '技术股为在职限制性干股，不出资。\n'
                '医生离职，股权自动收回，重新分配。'
            )
            self.result_label.text = txt
        except Exception as e:
            self.result_label.text = f'输入错误！\n{e}'


# ========== 主管理器 ==========
class MainManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ScreenProfit(name='screen_profit'))
        self.add_widget(ScreenStock(name='screen_stock'))


class PetHospitalCalcApp(App):
    def build(self):
        self.title = '宠物医院经营&股权测算'
        return MainManager()


if __name__ == '__main__':
    PetHospitalCalcApp().run()
