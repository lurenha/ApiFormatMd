# ApiFormatMd
## 配置项
- 作者 author = '江火似流萤'
- 载入类根目录 root_path = r"/Users/xxx" (这里指定java项目根目录,程序以此为起点遍历java文件)
- 生成md文件目录 write_path = r"/Users/xxx/Desktop"
- 参数写入param.txt 

## 例子
### java接口
<details>
<summary>查看代码</summary>

```java
    @RequestMapping(value = "/v1/test/{userId}", method = RequestMethod.POST)
    public JsonResult<InvoiceVO> test(
            @PathVariable(value = "userId") int userId,
            @RequestParam(value = "roleCode", required = true) String roleCode,
            @RequestBody QuoteStrategyRule quoteStrategyRule) {
        return new JsonResult<>();
    }
```
##### InvoiceVO
```java
@Data
public class InvoiceVO extends Invoice {

    //发票编号-子
    private Long invoiceNo;
    //发票标题-子
    private String invoiceTitle;

    /**
     * 发票类型-子
     */
    private InvoiceEnum invoiceEnum;

    //扩展信息
    private ExtendSub extendSub;

    @Data
    public static class Extend {
        //标题-父
        private String title;
        //内容-父
        private String content;

    }

    @Data
    public static class ExtendSub extends Extend {
        //spu集合-子
        private List<Spu> spuList;
        //spu信息-子
        private Spu spu;

        /**
         *  spu Map-子
         */

        private Map<String, Spu> spuMap;

        //渠道枚举
        private SpecialChannelEnum specialChannelEnum;

    }
}
```
##### Spu
```java
@Data
public class Spu implements Serializable {
    private static final long serialVersionUID = 128833531741299945L;
    /**
     * 主键ID
     */
    private long id;

    /**
     * 商品类别
     */
    private byte productType;

    /**
     * 商品子类别
     */
    private int productSubType;

    /**
     * spu中文名称
     */
    private String nameCn;

    /**
     * spu英文名称
     */
    private String nameEn;

    /**
     * poiId，按照poi_id顺序逗号分隔，eg：1,3,12
     */
    private String poiIds;

    /****** 业务字段 ********/

    /**
     * 多语言处理后显示的name，v1.5.1新增
     */
    private String name;

    /**
     * 创建人
     */
    private String createPin;


    /**
     * 更新人
     */

    private String updatePin;

    //key集合
    private List<Key> keyList;

}
```

##### Spu
```java
@Data
public class Key implements Serializable {
    private static final long serialVersionUID = 7585869752216827433L;
    private Integer pageSize;
    /**
     * 要素类别
     */
    private byte type;

    /**
     * 要素名称
     */
    private String name;

    /****** 业务字段 *******/
    /**
     * 要素名称多语言map
     * Map<languageCode, value>
     */
    private Map<String, String> names;

    private List<Key> keyList;
}
```
</details>


### 生成内容
<details>
<summary>查看内容</summary>

## 接口说明

|名称|描述|
|:--:|:--:|
|功能|**找不到名字了用这个吧**|
|负责人|**江火似流萤**|


## HTTP请求地址
- 地址: `http://domain//v1/test/{userId}`

### 请求方式
- POST

## 参数说明
### 请求参数说明

|参数名|类型|必填|示例|说明|
| :----: | :----: | :----: | :----: | :----: |
|roleCode|String|-|-|-|
|quoteStrategyRule|[QuoteStrategyRule](#QuoteStrategyRule)|-|-|-|
|userId|int|-|-|-|



### 返回参数说明

|参数名|类型|示例|说明|
| :----: | :----: | :----: | :----: |
|code|String|"0"|状态码(非0为异常情况)|
|message |String|请求成功|信息描述|
|data|[JsonResult](#JsonResult)<[InvoiceVO](#InvoiceVO)>|-|- |



### 补充实体说明
<h5 id="QuoteStrategyRule">QuoteStrategyRule</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|id|Long|-|-|-|
|quoteStrategyId|Long|-|-| 所属策略ID|
|resellerChannelId|Long|-|-| 所属渠道ID|
|quoteStrategyCategory|Byte|-|-| 所属分类 1 生活服务；2 酒店业务；3 飞机票价|
|type|Byte|-|-| 引用ID，类型为1是0; 类型为2是大类枚举值； 类型为3是子类枚举值；类型为4商品ID；类型为5是规格ID；类型为6是规格ID|
|name|String|-|-| 类型为1是【分类名称】; 类型为2是【分类名称>大类名称】；, 类型为3是【分类名称>大类名称>子类名称】；, 类型为4是【分类名称>商品id】；类型为5是【分类名称>商品id>规格id】；, 类型为6是【分类名称>商品id>规格id>开始时间~结束时间】|
|refId|Long|-|-| 引用ID，类型为1是0; 类型为2是大类枚举值； 类型为3是子类枚举值；类型为4商品ID；类型为5是规格ID；类型为6是规格ID|
|startDate|Date|-|-| 生效时间，类型为6时有值否则为null，格式yyyy-MM-dd HH:mm:ss|
|endDate|Date|-|-| 失效时间，类型为6时有值否则为nu，格式yyyy-MM-dd HH:mm:ss|
|priceType|Byte|-|-| 加价类型 1百分比 2固定金额|
|rate|Integer|-|-| 加价百分比，当加价类型为1时，该字段有值|
|amount|Integer|-|-| 加价金额，当加价类型为2时，该字段有值|
|createTime|Date|-|-| 创建时间|
|updateTime|Date|-|-| 更新时间|
|operator|String|-|-| 操作人|
---

<h5 id="JsonResult">JsonResult</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|code|Integer|-|-| code 为"0"则无异常|
|msg|String|-|-| msg|
|data|T|-|-| data 返回体对象|
---

<h5 id="InvoiceVO">InvoiceVO</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|invoiceId|Long|-|-|-|
|invoiceTitleType|Byte|-|-| 发票抬头类型 1：个人 2：单位|
|invoiceType|Byte|-|-| 发票类型 1：国内纸质发票 2：国内电子发票 3:国际电子发票|
|name|String|-|-| 个人名称|
|companyName|String|-|-| 单位名称|
|status|Byte|-|-| 发票状态 1：处理中 2：已开发票|
|taxRegisterNumber|String|-|-| 纳税人识别号|
|invoiceCode|String|-|-| 发票编号|
|invoiceAmount|Long|-|-| 发票金额|
|registerAddress|String|-|-| 单位注册地址|
|registerPhone|String|-|-| 单位注册电话|
|bankName|String|-|-| 开户银行|
|bankNo|String|-|-| 银行卡号|
|contactName|String|-|-| 收件人姓名|
|contactPhone|String|-|-| 收件人手机号|
|contactAddress|String|-|-| 收件人地址|
|contactEmail|String|-|-| 收件人邮箱|
|expressNo|String|-|-| 快递单号|
|expressName|String|-|-| 快递公司|
|fileUrl|String|-|-| 发票电子文件地址|
|filePath|String|-|-| 发票电子文件地址|
|supplierId|Integer|-|-| 实际供应商id|
|ownerId|Integer|-|-| ownerId|
|userId|Integer|-|-| userId|
|remark|String|-|-| 备注|
|yn|Boolean|-|-| 删除标识|
|createTime|Date|-|-| 创建时间|
|updateTime|Date|-|-| 更新时间|
|createPin|String|-|-| 创建人|
|updatePin|String|-|-| 更新人|
|invoiceNo|Long|-|-|发票编号-子|
|invoiceTitle|String|-|-|发票标题-子|
|invoiceEnum|[InvoiceEnum](#InvoiceEnum)|-|-| 发票类型-子|
|extendSub|[ExtendSub](#ExtendSub)|-|-|扩展信息|
---

<h5 id="ExtendSub">ExtendSub</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|title|String|-|-|标题-父|
|content|String|-|-|内容-父|
|spuList|List<[Spu](#Spu)>|-|-|spu集合-子|
|spu|[Spu](#Spu)|-|-|spu信息-子|
|spuMap|Map<String,[Spu](#Spu)>|-|-|  spu Map-子|
|specialChannelEnum|[SpecialChannelEnum](#SpecialChannelEnum)|-|-|渠道枚举|
---

<h5 id="InvoiceEnum">InvoiceEnum</h5>

```java
enum InvoiceEnum {
    PERSON(1, "抬头为个人"),
    COMPANY(2, "抬头为单位"),

    BEING(1, "发票状态处理中"),
    COMPLETE(2, "发票状态已完成"),

    PAPER(1, "纸质发票"),
    ELECTRONIC(2, "电子发票");
```
<h5 id="SpecialChannelEnum">SpecialChannelEnum</h5>

```java
enum SpecialChannelEnum implements CommonEnum{
    DEFAULT("DEFAULT", "默认渠道"),
    SASS("SASS", "SASS平台"),
    UNKNOWN("UNKNOWN", "UNKNOWN"),
    ;
```
<h5 id="Spu">Spu</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|id|long|-|-| 主键ID|
|productType|byte|-|-| 商品类别|
|productSubType|int|-|-| 商品子类别|
|nameCn|String|-|-| spu中文名称|
|nameEn|String|-|-| spu英文名称|
|poiIds|String|-|-| poiId，按照poi_id顺序逗号分隔，eg：1,3,12|
|name|String|-|-| 业务字段 , 多语言处理后显示的name，v1.5.1新增|
|createPin|String|-|-| 创建人|
|updatePin|String|-|-| 更新人|
|keyList|List<[Key](#Key)>|-|-|key集合|
---

<h5 id="Key">Key</h5>


|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |
|pageSize|Integer|-|-|-|
|type|byte|-|-| 要素类别|
|name|String|-|-| 要素名称|
|names|Map<String,String>|-|-| 业务字段 , 要素名称多语言map, Map<languageCode, value>|
|keyList|List<[Key](#Key)>|-|-|-|
---





</details>